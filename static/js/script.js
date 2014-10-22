$(function() {
	var currentDate = new Date();
	document.querySelector('#ride-date').value = currentDate.getFullYear() + "-" + (currentDate.getMonth()+1) + "-" + currentDate.getDate();

	// couldn't figure out a better way to do this...
	// currentDate.toISOString().substring(11,16) give you the time in wrong tiemzone
	// and toLocaleString() returns 00:00 as 12:00 so AM/PM mixup
	// hence the extra lines of code 
	var hours = currentDate.getHours();
	if (hours < 10) hours = "0" + hours;
	var minuets = currentDate.getMinutes();
	if (minuets < 10) minuets = "0" + minuets;
	document.querySelector('#ride-start-time').value = hours + ":" + minuets;
	console.log(hours+ ":" + currentDate.getMinutes());
	if ((hours++) < 10) hours = "0" + hours;
    document.querySelector('#ride-end-time').value = hours + ":" + minuets;
});