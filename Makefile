setup-map:
	cd map && \
	npm install && \
	ln -s ../exporter/geojson .

setup-exporter:
	cd exporter && \
	./get-shapes.sh && \
	./setup-venv.sh && \
	./setup-db.sh && \
	mkdir -p geojson

setup: setup-map setup-exporter

image-exporter: 
	cd exporter && \
	docker build -t wlw-partner-exporter .

image-map:
	cd map && \
	docker build -t wlw-partner-map .

images: image-map image-exporter

run-map:
	cd map && npm start

run-map-container:
	docker run --rm \
	--mount type=bind,source=./exporter/geojson,target=/usr/share/nginx/html/geojson,ro,relabel=shared \
	-p '8080:80' wlw-partner-map:latest	

run-exporter:
	cd exporter && ./run.sh

run-exporter-container:
	docker run --rm \
	--mount type=bind,source=./exporter/geojson,target=/opt/wlw-geojson-exporter/geojson,relabel=shared \
	--mount type=bind,source=./exporter/db,target=/opt/wlw-geojson-exporter/db,ro,relabel=shared \
	 wlw-partner-exporter:latest	
