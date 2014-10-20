window.onload = function () {
  var currentDate = new Date();
  var rideDate = document.getElementById('ride-date');
  var rideStartTime = document.getElementById('ride-start-time');
  var rideEndTime = document.getElementById('ride-end-time');
  console.log(currentDate.getFullYear() + "-" + (currentDate.getMonth()+1) + "-" + currentDate.getDate());
  //rideDate.setAttribute("value", currentDate.getFullYear() + "-" + (currentDate.getMonth()+1) + "-" + currentDate.getDate());
  rideDate.value = currentDate.getFullYear() + "-" + (currentDate.getMonth()+1) + "-" + currentDate.getDate();
  rideStartTime.value = currentDate.getHours() + ":" + currentDate.getMinutes();
  rideEndTime.value = (currentDate.getHours()+1) + ":" + currentDate.getMinutes();
}