FROM nodejs:18-alpine as build

WORKDIR /opt/wlw-partner-map

ADD . .

RUN npm install

FROM nginx:alpine

COPY --from=build /opt/wlw-partner-map /usr/share/nginx/html

VOLUME ./usr/share/nginx/html/geojson
