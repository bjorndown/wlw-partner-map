const statusToColor = {
  P: 'green',
  K: 'purple',
  I: 'red',
  undefined: '#BBB',
}

const statusToText = {
  P: 'Partner',
  K: 'Kreislaufpartner',
  I: 'Kein Interesse',
  undefined: 'Kein Partner',
}

const renderPopup = layer => {
  const { NAME, url, comment } = layer.feature.properties
  return `${NAME}
  ${url ? `<br/><a target="_blank" href="${url}">${url}</a>` : ''}
  ${comment ? `<br/>${comment}` : ''}`
}

const style = feature => {
  const status = feature.properties.status
  const color = statusToColor[status]
  const opacity = ['P', 'K'].includes(status) ? 1 : 0.5
  return { color, opacity }
}

L.Control.SearchBox = L.Control.extend({
  onAdd() {
    const container = L.DomUtil.create('div', 'autocomplete')
    container.id = 'suggest'
    L.DomEvent.disableClickPropagation(container)

    const input = L.DomUtil.create('input', 'autocomplete-input', container)
    input.type = 'text'

    L.DomUtil.create('ul', 'autocomplete-result-list', container)

    return container
  },
})

L.control.SearchBox = function (data, opts) {
  return new L.Control.SearchBox(data, opts)
}

const setupMap = data => {
  const merenschwandCenter = [47.25941, 8.37492]
  const initialZoomLevel = 10
  const maxZoom = 19
  const map = L.map('map', { zoomControl: false }).setView(
    merenschwandCenter,
    initialZoomLevel
  )
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)
  L.geoJSON(data, { style }).bindPopup(renderPopup).addTo(map)
  L.control.zoom({ position: 'bottomleft' }).addTo(map)
  L.control.SearchBox(data, { position: 'topright' }).addTo(map)
  return map
}

const setupAutoComplete = (map, data) => {
  new Autocomplete('#suggest', {
    search: searchString => {
      if (searchString.length < 3) {
        return []
      }

      return data.features.filter(feature =>
        feature.properties.NAME.toLowerCase().includes(searchString)
      )
    },
    renderResult: (feature, props) =>
      `<li ${props}>${feature.properties.NAME} (${
        statusToText[feature.properties.status]
      })</li>`,
    getResultValue: feature => feature.properties.NAME,
    onSubmit: feature => {
      if (!feature) {
        return
      }
      map.fitBounds(
        L.latLngBounds(
          feature.geometry.coordinates[0].map(lngLat =>
            L.GeoJSON.coordsToLatLng(lngLat)
          )
        )
      )
    },
    autoSelect: true,
  })
}

const response = await fetch('/geojson/partners.geojson')

if (response.ok) {
  const data = await response.json()
  const map = setupMap(data)
  setupAutoComplete(map, data)
} else {
  document.querySelector('#error').textContent = 'Could not load partner data'
}
