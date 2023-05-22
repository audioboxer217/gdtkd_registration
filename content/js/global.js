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
  var age = today.getFullYear() - dateString.split('/')[2]
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
  document.getElementById("ageClass").innerHTML = "Age Group is <b>" + ageClass + "</b>"
}
$(function () {
  $('#datepicker').datepicker();
});