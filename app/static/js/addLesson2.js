function addLesson() {
	var x = document.createElement("INPUT");
	x.setAttribute("type", "text");
	x.setAttribute("class", "form-control mt-3");
	x.setAttribute("name", "lessonTitle");
	x.setAttribute("id", "lessonTitle");
	document.getElementById('lesson-input').append(x);
}