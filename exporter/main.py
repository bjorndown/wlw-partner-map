import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass
from typing import List, Union

import numpy as np
import shapefile
from pyproj import Transformer
from shapely.geometry import Polygon

parser = argparse.ArgumentParser()
parser.add_argument('-o',
                    '--outfile',
                    help="where to write GeoJSON data",
                    default='./geojson/partners.geojson')
parser.add_argument('-d',
                    '--database',
                    help="path to partners database",
                    default='./db/partners.db')
args = parser.parse_args()

ESPG_LV95 = 'EPSG:2056'
EPSG_WGS84 = 'EPSG:4326'
transformer = Transformer.from_crs(ESPG_LV95, EPSG_WGS84, always_xy=True)

logger = logging.getLogger('partner-geojson-exporter')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

con = sqlite3.connect(args.database)


@dataclass
class Partner:
    status: str
    url: str
    comment: str


def find_partner(uuid: int) -> Union[Partner, None]:
    with con:
        cursor = con.execute(
            "SELECT status, url, comment FROM partners WHERE uuid = ?", (uuid, ))

        result = cursor.fetchone()
        if result:
            return Partner(result[0], result[1], result[2])


def simplify(points: List[tuple[float, float]]) -> List[tuple[float, float]]:
    '''Reduce number of points in polygon using https://shapely.readthedocs.io/en/stable/manual.html?highlight=simplify#object.simplify'''
    return [
        p for p in Polygon(np.array(points)).simplify(
            0.0025, preserve_topology=True).exterior.coords
    ]


def transform(points: List[tuple[float, float]]) -> List[tuple[float, float]]:
    '''Convert coordinates from LV95 to WGS84 using https://pyproj4.github.io/pyproj/dev/examples.html#step-2-create-transformer-to-convert-from-crs-to-crs'''
    return [transformer.transform(x, y) for x, y in points]


def get_geojson(shapeRecord: shapefile.ShapeRecords):
    geojson = shapeRecord.__geo_interface__
    del geojson['properties']['UUID']  # reduce file size ~0.1MB
    new_coords = simplify(transform(geojson['geometry']['coordinates'][0]))
    geojson['geometry']['coordinates'][0] = new_coords
    return geojson


logger.info("reading shapes")

# schema
# [('DeletionFlag', 'C', 1, 0), ['UUID', 'C', 38, 0], ['DATUM_AEND', 'D', 8, 0],
#  ['DATUM_ERST', 'D', 8, 0], ['ERSTELL_J', 'N', 10, 0],
#  ['ERSTELL_M', 'C', 20, 0], ['REVISION_J', 'N', 10, 0],
#  ['REVISION_M', 'C', 20, 0], ['GRUND_AEND', 'C', 20, 0],
#  ['HERKUNFT', 'C', 20, 0], ['HERKUNFT_J', 'N', 10, 0],
#  ['HERKUNFT_M', 'C', 20, 0], ['OBJEKTART', 'C', 20, 0],
#  ['BEZIRKSNUM', 'N', 10, 0], ['SEE_FLAECH', 'N', 31, 15],
#  ['REVISION_Q', 'C', 100, 0], ['NAME', 'C', 254, 0], ['KANTONSNUM', 'N', 10, 0],
#  ['ICC', 'C', 20, 0], ['EINWOHNERZ', 'N', 10, 0], ['BFS_NUMMER', 'N', 10, 0],
#  ['GEM_TEIL', 'C', 20, 0], ['GEM_FLAECH', 'N', 31, 15], ['SHN', 'C', 20, 0]]
sf = shapefile.Reader(
    'shapes/SHAPEFILE_LV95_LN02/swissBOUNDARIES3D_1_3_TLM_HOHEITSGEBIET')

fields = ('UUID', 'NAME')
collection = {'type': 'FeatureCollection', 'features': []}

logger.info("transform and merge")

for shapeRecord in sf.shapeRecords(fields=fields):
    geojson = get_geojson(shapeRecord)
    partner = find_partner(shapeRecord.record.UUID)

    if partner:
        geojson['properties']['status'] = partner.status
        geojson['properties']['url'] = partner.url
        geojson['properties']['comment'] = partner.comment

    collection['features'].append(geojson)

con.close()

logger.info("writing to %s", args.outfile)

with open(args.outfile, 'w') as outfile:
    json.dump(collection, outfile)

logger.info("done")