function imgError(image) {
    image.onerror = "";
    image.src = "/media/default2.jpg";
    return true;
}

function initMap() {
  // The location of Uluru
  var uluru = {lat: 34.0522, lng: -118.2437};
  // The map, centered at Uluru
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 4, center: uluru});
  // The marker, positioned at Uluru
  var marker = new google.maps.Marker({position: uluru, map: map})
}
