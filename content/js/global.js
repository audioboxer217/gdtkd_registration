function formatPhoneNumber(input) {
  // Remove any non-digits from the input
  var phoneNum = input.replace(/[^0-9]/g, "");

  // Check if the input is a valid phone number
  if (phoneNum.length !== 10) {
    return;
  }

  // Format the phone number
  phoneNumFormatted = phoneNum.substring(0, 3) + "-" + phoneNum.substring(3, 6) + "-" + phoneNum.substring(6);

  document.getElementById("inputPhone").value = phoneNumFormatted;
}
function updateCostDetails() {
  var blackBelt = "The first event for Black Belts is $100 and each additional event is $25"
  var colorBelt = "The first event for Color Belts is $90 and each additional event is $20"
  if (document.getElementById('blackBelt').checked) {
    document.getElementById("costDetail").innerHTML = blackBelt;
  }
  else {
    document.getElementById("costDetail").innerHTML = colorBelt;
  }
  updateTotal()
}
function updateEventList() {
  var eventList = []
  var checked_items = document.querySelectorAll('input[name="events"]:checked')
  for (i = 0; i < checked_items.length; i++) {
    eventList.push(checked_items[i].id)
  }
  document.getElementById("eventList").value = eventList.join()
  updateTotal()
}
function updateTotal() {
  if (
    document.querySelectorAll('input[name="beltRank"]:checked').length > 0 &&
    document.querySelectorAll('input[name="events"]:checked').length > 0
  ) {
    if (document.getElementById('blackBelt').checked) {
      var eventPrice = 25
      var total = 75
    }
    else {
      var eventPrice = 20
      var total = 70
    }
    total += eventPrice * document.querySelectorAll('input[name="events"]:checked').length
    document.getElementById("total").value = "$" + total
  }
  else if (
    document.querySelectorAll('input[name="beltRank"]:checked').length == 0 &&
    document.querySelectorAll('input[name="events"]:checked').length > 0
  ) {
    alert("Please choose a Belt Rank to get your Total")
  }
}
function convertWeight(amount, unit) {
  if (unit == 'lbs') {
    document.getElementById("weightKgs").value = (amount * 0.45359237).toFixed(2)
  }
  else if (unit == 'kgs') {
    document.getElementById("weightLbs").value = (amount / 0.45359237).toFixed(2)
  }
  else {
    console.log("Error, unsupported unit " + unit)
  }
}
function calculateAge(dateString) {
  var today = new Date()
  var birthdate = new Date(dateString)
  console.log(birthdate)
  var age = today.getFullYear() - birthdate.getFullYear()//dateString.split('/')[2]
  document.getElementById("inputAge").value = age
  if (age <= 5) {
    var ageClass = "Titan"
  }
  else if (age > 5 && age <= 7) {
    var ageClass = "Tiger"
  }
  else if (age > 7 && age <= 9) {
    var ageClass = "Dragon"
  }
  else if (age > 9 && age <= 11) {
    var ageClass = "Youth"
  }
  else if (age > 11 && age <= 14) {
    var ageClass = "Cadet"
  }
  else if (age > 14 && age <= 17) {
    var ageClass = "Junior"
  }
  else if (age > 17 && age <= 32) {
    var ageClass = "Senior"
  }
  else if (age > 32) {
    var ageClass = "Ultra"
  }
  formattedBirthdate = birthdate.toLocaleDateString("en-US", {
    month: "2-digit",
    day: "2-digit",
    year: "numeric"
  });
  $('#datepicker').datepicker('update', formattedBirthdate);
  document.getElementById("birthdate").value = formattedBirthdate
  document.getElementById("ageClass").innerHTML = "Age Group is <b>" + ageClass + "</b>"
}
$(function () {
  $('#datepicker').datepicker();
});
function register() {
  var formData = new FormData(document.forms.eventRegistration);
  console.log("Form Data:")
  result_txt = []
  for (var pair of formData.entries()) {
    console.log(pair[0] + ' : ' + pair[1]);
    result_txt.push(pair[0] + ' : ' + pair[1])
  }
  document.getElementById("result").innerHTML = result_txt.join();
  return true;
}
function initMap() {
  const CONFIGURATION = {
    "ctaTitle": "Checkout",
    "mapOptions": { "center": { "lat": 37.4221, "lng": -122.0841 }, "fullscreenControl": true, "mapTypeControl": false, "streetViewControl": true, "zoom": 11, "zoomControl": true, "maxZoom": 22, "mapId": "" },
    "mapsApiKey": "AIzaSyDvoCcg6x5TBJSbh_VTFmpBBPlGt0xs568",
    "capabilities": { "addressAutocompleteControl": true, "mapDisplayControl": false, "ctaControl": false }
  };
  const componentForm = [
    'location',
    'locality',
    'administrative_area_level_1',
    // 'country',
    'postal_code',
  ];

  const getFormInputElement = (component) => document.getElementById(component + '-input');
  const autocompleteInput = getFormInputElement('location');
  const autocomplete = new google.maps.places.Autocomplete(autocompleteInput, {
    fields: ["address_components", "geometry", "name"],
    types: ["address"],
  });
  autocomplete.addListener('place_changed', function () {
    const place = autocomplete.getPlace();
    if (!place.geometry) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      window.alert('No details available for input: \'' + place.name + '\'');
      return;
    }
    fillInAddress(place);
  });

  function fillInAddress(place) {  // optional parameter
    const addressNameFormat = {
      'street_number': 'short_name',
      'route': 'long_name',
      'locality': 'long_name',
      'administrative_area_level_1': 'short_name',
      // 'country': 'long_name',
      'postal_code': 'short_name',
    };
    const getAddressComp = function (type) {
      for (const component of place.address_components) {
        if (component.types[0] === type) {
          return component[addressNameFormat[type]];
        }
      }
      return '';
    };
    getFormInputElement('location').value = getAddressComp('street_number') + ' '
      + getAddressComp('route');
    for (const component of componentForm) {
      // Location field is handled separately above as it has different logic.
      if (component !== 'location') {
        getFormInputElement(component).value = getAddressComp(component);
      }
    }
  }
}