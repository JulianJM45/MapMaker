// #0 constants
const POL_CF = 40007863; // Earth's circumference around poles
const ECF = 40075016.686; // Earth's circumference around equator

// console.log = function(message) {
//     var logDiv = document.getElementById('log');
//     var messageDiv = document.createElement('div');
//     messageDiv.textContent = message;
//     logDiv.appendChild(messageDiv);
// };
// console.log('Hello, World!');

// #1 configuration
const elementIds = {
    widthInput: 'width',
    heightInput: 'height',
    scaleInput: 'scale',
    autoZoomCheckbox: 'AutoZoom',
    zoomLabel: 'zoomLabel',
    zoomInput: 'zoom',
    showZoomLevelButton: 'showZoomLevel',
    upscaleCheckbox: 'Upscale',
    overviewCheckbox: 'Overview',
};
const elements = {};
for (let key in elementIds) {
    elements[key] = document.getElementById(elementIds[key]);
}

let config = {
    width: parseFloat(elements.widthInput.value),
    height: parseFloat(elements.heightInput.value),
    scale: parseFloat(elements.scaleInput.value),
    zoom: parseInt(elements.zoomInput.value),
    autoZoom: elements.autoZoomCheckbox.checked,
    upscale: elements.upscaleCheckbox.checked,
    overview: elements.overviewCheckbox.checked,
    pdf: true,  // This value isn't in your HTML, so we'll just set it to true
};

// switch button
var btn = document.getElementById('btn')
function leftClick() {
    btn.style.left = '0';
    config.pdf = true;
}
function rightClick() {
    btn.style.left = '50%';
    config.pdf = false;
}

// Apply the blur effect by default
elements.zoomLabel.style.filter = "blur(2px)";
elements.zoomInput.style.filter = "blur(2px)";
elements.showZoomLevelButton.style.filter = "blur(2px)";


// add event listeners
elements.widthInput.addEventListener('input', updateConfiguration);
elements.heightInput.addEventListener('input', updateConfiguration);
elements.scaleInput.addEventListener('input', updateConfiguration);
elements.autoZoomCheckbox.addEventListener('change', updateConfiguration);
elements.zoomInput.addEventListener('input', updateConfiguration);
elements.showZoomLevelButton.addEventListener('click', showZoomLevel);
elements.upscaleCheckbox.addEventListener('change', updateConfiguration);
elements.overviewCheckbox.addEventListener('change', updateConfiguration);

function toggleConfiguration() {
    const configForm = document.getElementById('configuration-form');
    configForm.style.display = configForm.style.display === 'none' ? 'block' : 'none';
}

elements.autoZoomCheckbox.addEventListener('change', function () {
    AutoZoom = this.checked;
    if (AutoZoom) {
        elements.zoomInput.disabled = true;
        elements.showZoomLevelButton.disabled = true;
        elements.zoomLabel.disabled = true; 
        elements.zoomInput.style.filter = "blur(2px)";  // Add blur effect
        elements.showZoomLevelButton.style.filter = "blur(2px)";  // Add blur effect
        elements.zoomLabel.style.filter = "blur(2px)";
    } else {
        elements.zoomInput.disabled = false;
        elements.showZoomLevelButton.disabled = false;
        elements.zoomLabel.disabled = false; 
        elements.zoomInput.style.filter = "none";  // Remove blur effect
        elements.showZoomLevelButton.style.filter = "none";  // Remove blur effect
        elements.zoomLabel.style.filter = "none";
    }
});

function updateConfiguration() {
    config.width = parseFloat(document.getElementById('width').value);
    config.height = parseFloat(document.getElementById('height').value);
    config.scale = parseFloat(document.getElementById('scale').value);
    config.zoom = parseInt(document.getElementById('zoom').value);
    config.autoZoom = document.getElementById('AutoZoom').checked;
    config.upscale = document.getElementById('Upscale').checked;
    config.overview = document.getElementById('Overview').checked;

}
function showZoomLevel() {
    const z = parseInt(document.getElementById('zoom').value);
    map.setZoom(z);
}




// #2 map
var map = L.map('map').setView([50.604, 10.887], 7);
// var map = L.map('map').setView([49.3497, 8.1429], 12);

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
// Add all tile layers to the map
outdooractiveST.addTo(map);
outdooractiveAUT.addTo(map);
outdooractiveDE.addTo(map);
openStreetMapLayer.addTo(map);
// check if opentopomap is available
fetch('https://tile.opentopomap.org/')
    .then(response => {
        if (response.ok) {
            openTopoMapLayer.addTo(map);
        } else {
            console.log('Website is not available');
        }
    })
    .catch(error => {
        console.log('An error occurred while checking the website availability:', error);
    });

// Create a layer control and add it to the map
var baseMaps = {
    "OutdooractiveSüdTirol": outdooractiveST,
    "OutdooractiveAUT": outdooractiveAUT,
    "OutdooractiveDE": outdooractiveDE,
    "OpenTopoMap": openTopoMapLayer,
    "OpenStreetMap": openStreetMapLayer,
};
L.control.layers(baseMaps).addTo(map);


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




// #3 create rectangles
function getBoundsFromMeters(bounds, widthMeters, heightMeters) {
    var centerLat = bounds.getCenter().lat;
    var centerLng = bounds.getCenter().lng;
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
function getMetersFromBounds(bounds) {
    const North = bounds.getNorth();
    const South = bounds.getSouth();
    const East = bounds.getEast();
    const West = bounds.getWest();
    const widthMeters = (East - West) * (ECF * Math.cos((North+South)/2 * (Math.PI / 180))) / 360;
    const heightMeters = (North - South) * POL_CF / 360;

    return [widthMeters, heightMeters];
}

var drawnRectangles = [];  // Array to store drawn rectangles
// Event handler for the draw:created event
map.on('draw:created', function (e) {
    // console.log('Rectangle created');
    var newRectangle = e.layer; // Store the new drawn rectangle

    // Set the rectangle to the fixed size
    var bounds = newRectangle.getBounds();
    // console.log('Center point: ' + 'Lat: ' + center.lat + ', Lng: ' + center.lng);
    var widthMeters = config.width * config.scale/1000;
    var heightMeters = config.height * config.scale/1000;

    const fixedSizeBounds = getBoundsFromMeters(bounds, widthMeters, heightMeters);
    newRectangle.setBounds(fixedSizeBounds);
    drawnRectangles.push(newRectangle);
    // Add the rectangle to the editable feature group
    editableLayers.addLayer(newRectangle);
    

    // #4 edit rectangles
    newRectangle.on('edit', function (e) {
 
        var bounds = newRectangle.getBounds();
        // console.log('Northeast point: ' + bounds.getNorthEast().toString());
        // console.log('Southwest point: ' + bounds.getSouthWest().toString());
        var [widthMeters, heightMeters] = getMetersFromBounds(bounds);
        var k = (config.width * heightMeters) / (config.height * widthMeters);
        if (Math.abs(k - 1) < 0.01) {
        } else {
            if (k > 1) {
                console.log('increased height');
                const newWidthMeters = heightMeters * config.width / config.height;
                const fixedSizeBounds = getBoundsFromMeters(bounds, newWidthMeters, heightMeters);
                newRectangle.setBounds(fixedSizeBounds);
            } else { 
                console.log('increased width');
                const newHeightMeters = widthMeters * config.height / config.width;
                const fixedSizeBounds = getBoundsFromMeters(bounds, widthMeters, newHeightMeters);
                newRectangle.setBounds(fixedSizeBounds);
            }
        }
        
    });


});







// #5 send coordinates

function sendCoordinates() {
    console.log("sending coordinates...");
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
    window.pywebview.api.send_coordinates(coordinates_List, selectedTileLayer, config.width, config.height, config.scale, config.zoom, config.upscale, config.overview, config.autoZoom, config.pdf);
}