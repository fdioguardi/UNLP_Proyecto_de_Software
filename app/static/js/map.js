var marker;
var map;
var result;
var direccion;

const mapClickHandler = (e) => {
    var geocodeService = L.esri.Geocoding.geocodeService();
    results.clearLayers();
    marker = L.marker(e.latlng)
    results.addLayer(marker)
    geocodeService.reverse().latlng(e.latlng).run(function (error, result) {
        if (error) {
            return;
        }
        direccion = result.address.Match_addr;
        document.getElementById('address').setAttribute('value', direccion);
    });
    latlng = marker.getLatLng();
    document.getElementById('lat').setAttribute('value', latlng.lat); //obtenemos el imput 
    document.getElementById('lng').setAttribute('value', latlng.lng);

}
const clickManual = (lat,lng) => {
    var geocodeService = L.esri.Geocoding.geocodeService();
    results.clearLayers();
    marker = L.marker([lat,lng])
    results.addLayer(marker)
    geocodeService.reverse().latlng([lat,lng]).run(function (error, result) {
        if (error) {
            return;
        }
        direccion = result.address.Match_addr;
        document.getElementById('address').setAttribute('value', direccion);
    });
    latlng = marker.getLatLng();
    document.getElementById('lat').setAttribute('value', lat); //obtenemos el imput 
    document.getElementById('lng').setAttribute('value', lng);

}
const initializeMap = (selector) => {
    var lat = document.getElementById('lat').getAttribute('value');
    var lng = document.getElementById('lng').getAttribute('value');
    map = L.map(selector).setView([-34.9187, -57.956], 13);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(map);
    map.on('click', mapClickHandler); //agrega el evento click ppara seleccionar un punto
    var searchControl = L.esri.Geocoding.geosearch().addTo(map);
    results = L.layerGroup().addTo(map);
    searchControl.on("results", function (data) {
        results.clearLayers();
        if (data.results.length > 0) {
            marker = L.marker(data.results[0].latlng)
            results.addLayer(marker)
        }
        var geocodeService = L.esri.Geocoding.geocodeService();
        geocodeService.reverse().latlng(data.results[0].latlng).run(function (error, result) {
            if (error) {
                return;
            }
            direccion = result.address.Match_addr;
            document.getElementById('address').setAttribute('value', direccion);
        });
        latlng = marker.getLatLng();
        document.getElementById('lat').setAttribute('value', latlng.lat); //obtenemos el imput 
        document.getElementById('lng').setAttribute('value', latlng.lng);
    })
    clickManual(lat,lng);
};

const submitHandler = (event) => {
    if (!marker) {
        event.preventDefault();
        alert('Se debe seleccionar un punto en el mapa')
    }
};

window.onload = () => {
    initializeMap('mapid');
    
};