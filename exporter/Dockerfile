FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl unzip

WORKDIR /opt/wlw-geojson-exporter

VOLUME ./geojson
VOLUME ./db

ADD . .

RUN ./get-shapes.sh

RUN pip install virtualenv && ./setup-venv.sh
  
CMD ["./run.sh"]
