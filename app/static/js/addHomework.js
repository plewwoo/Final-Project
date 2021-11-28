function addHomework() {
	var y = document.createElement("INPUT");
	y.setAttribute("class", "form-control mt-3");
	y.setAttribute("type", "text");
	y.setAttribute("name", "homeworkTitleTitle");
	y.setAttribute("id", "homeworkTitleTitle");
	document.getElementById('homeworkTitle-input').append(y);

	var x = document.createElement("INPUT");
	x.setAttribute("type", "file");
	x.setAttribute("class", "form-control mt-3");
	x.setAttribute("name", "homework");
	x.setAttribute("id", "homework");
	document.getElementById('homework-input').append(x);
}