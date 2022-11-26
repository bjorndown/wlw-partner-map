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
	podman build -t wlw-partner-exporter .

image-map:
	cd map && \
	podman build -t wlw-partner-map .

images: image-map image-exporter

