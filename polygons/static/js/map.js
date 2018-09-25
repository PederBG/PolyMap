
// Init map
let mymap = L.map('map').setView([51.505, -0.09], 12);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoicGVkZXJiZyIsImEiOiJjam0zeWIydXcxZTd3M3JteXhkN25yZzQyIn0.hUyDzVHO8hS8tuNPF4PpDw'
}).addTo(mymap);


// Add polygons
Object.keys(storedGrids).forEach(function(key) {
  let p = L.polygon([ swapCoords( storedGrids[key] ) ]); // Making polygons
  p.id = key;
  p.addTo(mymap);
  p.on('click', onPolyClick);
});

selectedPolygons = [];


// Help functions

// Handler for polygon onClick event
function onPolyClick(poly){
  index = selectedPolygons.indexOf(this.id);

  if (index == -1){
    selectedPolygons.push(this.id);
    this.setStyle({fillOpacity: 0.6});
  }
  else{
    selectedPolygons.splice(index, 1)
    this.setStyle({fillOpacity: 0.2});
  }
  togglePopup();
}

// Toggles menu for union and intersect
function togglePopup(){
  if (selectedPolygons.length > 1) $('.popup-menu').show();
  else $('.popup-menu').hide();
}

// Swapping coordinates since geojson use east,north while leaflet uses north,east
function swapCoords(coords){
  swapped = [];
  coords.forEach(function(coord) {
    swapped.push([coord[1], coord[0]]);
  });
  return swapped;
}

// Override default alert function
alert = function(str) {
  bootbox.alert({
    message: str,
    size: 'small',
    backdrop: true
  });
}
