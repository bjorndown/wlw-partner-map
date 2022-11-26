import 'leaflet'

const resp = await fetch('/geojson/partners.geojson')
const data = await resp.json()

const merenschwandCenter = [47.25941, 8.37492]
const initialZoomLevel = 10
const map = L.map('map').setView(merenschwandCenter, initialZoomLevel)

const renderPopup = layer => {
  const { NAME, url, comment, BFS_NUMMER } = layer.feature.properties
  return `${NAME} ${BFS_NUMMER}
  ${url ? `<br/><a target="_blank" href="${url}">${url}</a>` : ''}
  ${comment ? `<br/>${comment}` : ''}`
}

const style = feature => {
  const color =
    feature.properties.status === 'P'
      ? 'green'
      : feature.properties.status === 'I'
      ? 'red'
      : '#BBB'
  return { color }
}

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map)

L.geoJSON(data, {
  style,
})
  .bindPopup(renderPopup)
  .addTo(map)
