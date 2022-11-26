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
                    required=True,
                    help="where to write GeoJSON data")
args = parser.parse_args()

ESPG_LV95 = 'EPSG:2056'
EPSG_WGS84 = 'EPSG:4326'
transformer = Transformer.from_crs(ESPG_LV95, EPSG_WGS84, always_xy=True)

logger = logging.getLogger('partner-geojson-exporter')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

con = sqlite3.connect('db/partners.db')


@dataclass
class Partner:
    zip_code: int
    status: str
    url: str
    comment: str


def find_partner(zip_code: int) -> Union[Partner, None]:
    with con:
        cursor = con.execute(
            "SELECT zip_code, status, url, comment FROM partners WHERE zip_code = ?",
            (zip_code, ))

        result = cursor.fetchone()
        if result:
            return Partner(result[0], result[1], result[2], result[3])


def simplify(points: List[tuple[float, float]]) -> List[tuple[float, float]]:
    return [
        p for p in Polygon(np.array(points)).simplify(
            0.0025, preserve_topology=True).exterior.coords
    ]


def transform(points: List[tuple[float, float]]) -> List[tuple[float, float]]:
    return [transformer.transform(x, y) for x, y in points]


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

fields = ('NAME', 'BFS_NUMMER')
collection = {'type': 'FeatureCollection', 'features': []}

logger.info("transform and merge")

for shape in sf.shapeRecords(fields=fields):
    geojson = shape.__geo_interface__
    new_coords = simplify(transform(geojson['geometry']['coordinates'][0]))
    geojson['geometry']['coordinates'][0] = new_coords

    partner = find_partner(geojson['properties']['BFS_NUMMER'])

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