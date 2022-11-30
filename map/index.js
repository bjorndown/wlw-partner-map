const merenschwandCenter = [47.25941, 8.37492]
const initialZoomLevel = 10
const maxZoom = 19

const statusToColor = {
  P: 'green',
  K: 'purple',
  I: 'red',
  unknown: '#BBB',
}

const renderPopup = layer => {
  const { NAME, url, comment } = layer.feature.properties
  return `${NAME}
  ${url ? `<br/><a target="_blank" href="${url}">${url}</a>` : ''}
  ${comment ? `<br/>${comment}` : ''}`
}

const style = feature => {
  const status = feature.properties.status ?? 'unknown'
  const color = statusToColor[status]
  const opacity = ['P', 'K'].includes(status) ? 1 : 0.5
  return { color, opacity }
}

const response = await fetch('/geojson/partners.geojson')

if (response.ok) {
  const data = await response.json()

  const map = L.map('map').setView(merenschwandCenter, initialZoomLevel)

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)

  L.geoJSON(data, {
    style,
  })
    .bindPopup(renderPopup)
    .addTo(map)
} else {
  document.querySelector('#error').textContent = 'Could not load partner data'
}
