const response = await fetch('/geojson/partners.geojson')

if (!response.ok) {
  document.querySelector('#error').textContent = 'Could not load GeoJSON data'
}

const data = await response.json()

const merenschwandCenter = [47.25941, 8.37492]
const initialZoomLevel = 10
const map = L.map('map').setView(merenschwandCenter, initialZoomLevel)

const renderPopup = layer => {
  const { NAME, url, comment } = layer.feature.properties
  return `${NAME}
  ${url ? `<br/><a target="_blank" href="${url}">${url}</a>` : ''}
  ${comment ? `<br/>${comment}` : ''}`
}

const style = feature => {
  const { status } = feature.properties
  const color = status === 'P' ? 'green' : status === 'I' ? 'red' : '#BBB'

  const opacity = status === 'P' ? 1 : 0.5
  return { color, opacity }
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
