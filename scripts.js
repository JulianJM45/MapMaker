var width = 288;
var height = 201;
var scale = 25000;
var zoom = 14;
var AutoZoom = true;
var upscale = false;
var Overview = false;
var PDF = true;

// Add event listeners for the checkboxes and button
const widthInput = document.getElementById('width');
const heightInput = document.getElementById('height');
const scaleInput = document.getElementById('scale');
const autoZoomCheckbox = document.getElementById('AutoZoom');
const zoomLabel = document.getElementById('zoomLabel');
const zoomInput = document.getElementById('zoom');
const showZoomLevelButton = document.getElementById('showZoomLevel');
const upscaleCheckbox = document.getElementById('Upscale');
const overviewCheckbox = document.getElementById('Overview');

widthInput.addEventListener('input', updateConfiguration);
heightInput.addEventListener('input', updateConfiguration);
scaleInput.addEventListener('input', updateConfiguration);
autoZoomCheckbox.addEventListener('change', updateConfiguration);
zoomInput.addEventListener('input', updateConfiguration);
showZoomLevelButton.addEventListener('click', showZoomLevel);
upscaleCheckbox.addEventListener('change', updateConfiguration);
overviewCheckbox.addEventListener('change', updateConfiguration);

function toggleConfiguration() {
    const configForm = document.getElementById('configuration-form');
    configForm.style.display = configForm.style.display === 'none' ? 'block' : 'none';
}

// switch button
var btn = document.getElementById('btn')

function leftClick() {
    btn.style.left = '0';
    PDF = true;
}

function rightClick() {
    btn.style.left = '50%';
    PDF = false;
}
// Apply the blur effect by default
zoomLabel.style.filter = "blur(2px)";
zoomInput.style.filter = "blur(2px)";
showZoomLevelButton.style.filter = "blur(2px)";
// Add an event listener to the AutoZoom checkbox
// const autoZoomCheckbox = document.getElementById('AutoZoom');
autoZoomCheckbox.addEventListener('change', function () {
    AutoZoom = this.checked;
    if (AutoZoom) {
        zoomInput.disabled = true;
        showZoomLevelButton.disabled = true;
        zoomLabel.disabled = true; 
        zoomInput.style.filter = "blur(2px)";  // Add blur effect
        showZoomLevelButton.style.filter = "blur(2px)";  // Add blur effect
        zoomLabel.style.filter = "blur(2px)";
    } else {
        zoomInput.disabled = false;
        showZoomLevelButton.disabled = false;
        zoomLabel.disabled = false; 
        zoomInput.style.filter = "none";  // Remove blur effect
        showZoomLevelButton.style.filter = "none";  // Remove blur effect
        zoomLabel.style.filter = "none";
    }
});

function updateConfiguration() {
    width = parseFloat(document.getElementById('width').value);
    height = parseFloat(document.getElementById('height').value);
    scale = parseFloat(document.getElementById('scale').value);
    zoom = parseInt(document.getElementById('zoom').value);
    AutoZoom = document.getElementById('AutoZoom').checked;
    upscale = document.getElementById('Upscale').checked;
    Overview = document.getElementById('Overview').checked;

}
function showZoomLevel() {
    const z = parseInt(document.getElementById('zoom').value);
    map.setZoom(z);
}

var map = L.map('map').setView([49.3497, 8.1429], 12);
var openTopoMapLayer = L.tileLayer('https://tile.opentopomap.org/{z}/{x}/{y}.png', {
    name: 'tile.opentopomap.org' // Set the name property
});
var openStreetMapLayer = L.tileLayer('https://tile.openstreetmap.de/{z}/{x}/{y}.png', {
    name: 'a.tile.openstreetmap.de' // Set the name property
});
var outdooractiveDE = L.tileLayer('https://t0.outdooractive.com/portal/map/{z}/{x}/{y}.png', {
    name: 't0.outdooractive.com/portal/map' // Set the name property
});
var outdooractiveAUT = L.tileLayer('https://t0.outdooractive.com/austria/map/{z}/{x}/{y}.png', {
    name: 't0.outdooractive.com/austria/map' // Set the name property
});
var outdooractiveST = L.tileLayer('https://t0.outdooractive.com/suedtirol/map/{z}/{x}/{y}.png', {
    name: 't0.outdooractive.com/suedtirol/map' // Set the name property
});
// Add both tile layers to the map
outdooractiveST.addTo(map);
outdooractiveAUT.addTo(map);
outdooractiveDE.addTo(map);
// openTopoMapLayer.addTo(map);
openStreetMapLayer.addTo(map);

// Create a layer control and add it to the map
var baseMaps = {
    "OutdooractiveSüdTirol": outdooractiveST,
    "OutdooractiveAUT": outdooractiveAUT,
    "OutdooractiveDE": outdooractiveDE,
    "OpenTopoMap": openTopoMapLayer,
    "OpenStreetMap": openStreetMapLayer,
};

// Create a search control and add it to the map
var searchControl = L.Control.geocoder({
    defaultMarkGeocode: true, // Don't add a marker for the search result by default
    position: 'topleft', // Set the position to top-left
}).addTo(map);

// Event handler for when a location is found
searchControl.on('markgeocode', function (e) {
    var latlng = e.geocode.center; // Get the coordinates of the search result
    var marker = L.marker(latlng).addTo(map); // Add a marker to the found location
});

L.control.layers(baseMaps).addTo(map);


// Initialize Leaflet.draw and Leaflet.Editable
var editableLayers = new L.FeatureGroup(); // Create a feature group for editable layers
map.addLayer(editableLayers);

var drawOptions = {
    draw: {
        rectangle: true,
        polyline: false,
        circle: false,
        polygon: false,
        marker: true,
        circlemarker: false,
    },
    edit: {
        featureGroup: editableLayers, // Add the editable features to the map
        edit: true,        // Enable editing
        remove: true       // Enable deleting
    }
};

var drawControl = new L.Control.Draw(drawOptions);
map.addControl(drawControl);

var drawnRectangles = [];  // Array to store drawn rectangles
// Event handler for the draw:created event
map.on('draw:created', function (e) {
    var newRectangle = e.layer; // Store the new drawn rectangle
    map.addLayer(newRectangle);

    // Disable resizing handles for the drawn rectangle
    newRectangle.editing.disable();

    // Set the rectangle to the fixed size
    var center = newRectangle.getBounds().getCenter();
    var widthMeters = width * scale/1000;
    var heightMeters = height * scale/1000;

    function getBoundsFromMeters(centerLat, centerLng, widthMeters, heightMeters, zoomLevel) {
        const POL_CF = 40007863; // Earth's circumference around poles
        const ECF = 40075016.686; // Earth's circumference around equator
        const latRadians = centerLat * (Math.PI / 180); // Convert latitude to radians
        const widthHalf = widthMeters / 2;
        const heightHalf = heightMeters / 2;

        // Calculate the change in longitude (degrees) for the given width in meters
        const lngDeltaHalf = (widthHalf / (ECF * Math.cos(latRadians))) * 360;

        // Calculate the change in latitude (degrees) for the given height in meters
        const latDeltaHalf = (heightHalf / POL_CF) * 360;

        // Calculate the new bounds
        const southWest = L.latLng(centerLat - latDeltaHalf, centerLng - lngDeltaHalf);
        const northEast = L.latLng(centerLat + latDeltaHalf, centerLng + lngDeltaHalf);

        return L.latLngBounds(southWest, northEast);
    }

    const fixedSizeBounds = getBoundsFromMeters(center.lat, center.lng, widthMeters, heightMeters, 11);
    newRectangle.setBounds(fixedSizeBounds);
    drawnRectangles.push(newRectangle);
    // Add the rectangle to the editable feature group
    editableLayers.addLayer(newRectangle);
});

function sendCoordinates() {
    console.log("This is a log message");
    var coordinates_List = [];

    // Get the currently selected tile layer
    var selectedTileLayer = null;

    // Iterate through all tile layers added to the map
    map.eachLayer(function (layer) {
        if (layer instanceof L.TileLayer && map.hasLayer(layer)) {
            // Check if the layer is an instance of L.TileLayer and is currently active
            if (layer.options && layer.options.name) {
                selectedTileLayer = layer.options.name;
            }
        }
    });

    // Iterate through the drawn rectangles and extract their coordinates
    drawnRectangles.forEach(function (rectangle) {
        if (editableLayers.hasLayer(rectangle)) {  // Check if the rectangle is still active
            var bounds = rectangle.getBounds();
            var NorthWest = bounds.getNorthWest();
            var SouthEast = bounds.getSouthEast();

            var coordinates = {
                Northwest: [NorthWest.lat, NorthWest.lng],
                SouthEast: [SouthEast.lat, SouthEast.lng]
            };
            coordinates_List.push(coordinates);
        }
    });

    // Call the Python function to send the coordinates
    window.pywebview.api.send_coordinates(coordinates_List, selectedTileLayer, width, height, scale, zoom, upscale, Overview, AutoZoom, PDF);
}
