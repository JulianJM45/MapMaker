document.addEventListener('DOMContentLoaded', function() {

    

 // #1 add map
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




// #2 log output
function showMessage(message) {
    // console.log(message);
    document.getElementById('log').innerText = message;
}
showMessage('Hello, World!');




// #3 map tools

// Create a search control and add it to the map
var searchControl = L.Control.geocoder({
    defaultMarkGeocode: true, 
    position: 'topleft', 
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

// load GPX track
// Get the button and file input elements
var gpxButton = document.getElementById('gpxButton');
var gpxFileInput = document.getElementById('gpxFileInput');

// Add an event listener for the 'click' event to the button
gpxButton.addEventListener('click', function() {
    // Trigger the file input's click event
    gpxFileInput.click();
});

// Add an event listener for the 'change' event to the file input
gpxFileInput.addEventListener('change', function(e) {
    var file = e.target.files[0];
    var reader = new FileReader();

    // Add an event listener for the 'load' event
    reader.addEventListener('load', function(e) {
        var gpxData = e.target.result;

        // Load the GPX data into the map
        new L.GPX(gpxData, {async: true}).on('loaded', function(e) {
            map.fitBounds(e.target.getBounds());
        }).addTo(map);
    });
    reader.readAsText(file);
});




// #4 configuration

// toggle configuration form
const configureButton = document.getElementById('configure-button');
    const configurationForm = document.getElementById('configuration-form');

    configureButton.addEventListener('click', function() {
        if (configurationForm.style.display === 'none' || configurationForm.style.display === '') {
            configurationForm.style.display = 'block';
        } else {
            configurationForm.style.display = 'none';
        }
    });

// get elements
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

const elements = Object.fromEntries(
    Object.entries(elementIds).map(([key, id]) => [key, document.getElementById(id)])
);

let config = {
    width: parseFloat(elements.widthInput.value),
    height: parseFloat(elements.heightInput.value),
    scale: parseFloat(elements.scaleInput.value),
    zoom: parseInt(elements.zoomInput.value),
    autoZoom: elements.autoZoomCheckbox.checked,
    upscale: elements.upscaleCheckbox.checked,
    overview: elements.overviewCheckbox.checked,
    pdf: false,  
};


// Apply the blur effect by default
['zoomLabel', 'zoomInput', 'showZoomLevelButton'].forEach(id => {
    elements[id].style.filter = "blur(2px)";
});

// switch button
var btn = document.getElementById('btn')
function leftClick() {
    btn.style.left = '0';
    config.pdf = false;
}
function rightClick() {
    btn.style.left = '50%';
    config.pdf = true;
}

// Show the current zoom level
function showZoomLevel() {
    const z = parseInt(document.getElementById('zoom').value);
    map.setZoom(z);
}

// Update configuration function
function updateConfiguration() {
    Object.assign(config, {
        width: parseFloat(elements.widthInput.value),
        height: parseFloat(elements.heightInput.value),
        scale: parseFloat(elements.scaleInput.value),
        zoom: parseInt(elements.zoomInput.value),
        autoZoom: elements.autoZoomCheckbox.checked,
        upscale: elements.upscaleCheckbox.checked,
        overview: elements.overviewCheckbox.checked,
    });
}


// Add event listeners
['widthInput', 'heightInput', 'scaleInput', 'zoomInput'].forEach(id => {
    elements[id].addEventListener('input', updateConfiguration);
});
['autoZoomCheckbox', 'upscaleCheckbox', 'overviewCheckbox'].forEach(id => {
    elements[id].addEventListener('change', updateConfiguration);
});
elements.showZoomLevelButton.addEventListener('click', showZoomLevel);

elements.autoZoomCheckbox.addEventListener('change', function () {
    const isAutoZoom = this.checked;
    ['zoomInput', 'showZoomLevelButton', 'zoomLabel'].forEach(id => {
        elements[id].disabled = isAutoZoom;
        elements[id].style.filter = isAutoZoom ? "blur(2px)" : "none";
    });
});
document.getElementById('leftButton').addEventListener('click', leftClick);
document.getElementById('rightButton').addEventListener('click', rightClick);




// #5 create rectangles

const POL_CF = 40007863; // Earth's circumference around poles
const ECF = 40075016.686; // Earth's circumference around equator

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

// draw rectangle
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
    

    // # edit rectangles
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




// #6 send coordinates

document.getElementById('download-button').addEventListener('click', function(event) {
    event.preventDefault();
    prepareAndSendData().then(result => {
        console.log('Data sent successfully:', result);
    }).catch(error => {
        console.error('Failed to send data:', error);
    });
});

function prepareAndSendData() {
    document.getElementById('log').style.zIndex = "1000";
    document.getElementById('configuration-form').style.display = 'none';
    // console.log("sending coordinates...");
    showMessage('Sending coordinates...');


    // Iterate through the drawn rectangles and extract their coordinates
    var coordinates_List = [];
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

    // Prepare the data to be sent
    var data = {
        coordinates_list: coordinates_List,
        config: {
            tile_layer: selectedTileLayer,
            width: config.width,
            height: config.height,
            scale: config.scale,
            zoom: config.zoom,
            autoZoom: config.autoZoom,
            upscale: config.upscale,
            overview: config.overview,
            pdf: config.pdf
        }
    };

    return sendData(data);

}

function sendData(data) {
    // Send the data to the Flask backend using fetch
    fetch('/send_coordinates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // showMessage('Coordinates sent successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        showMessage('An error occurred while sending the coordinates.');
    });
}


// #7 socket.io
const socket = io();

socket.on('py-js_communication', function(message) {
    // resultParagraph.textContent = `Result: ${data.result}`;
    showMessage(message);
});



});