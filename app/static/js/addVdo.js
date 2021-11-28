function addVdo() {
	var y = document.createElement("INPUT");
	y.setAttribute("class", "form-control mt-3");
	y.setAttribute("type", "text");
	y.setAttribute("name", "videoTitle");
	y.setAttribute("id", "videoTitle");
	document.getElementById('videoTitle-input').append(y);

	var x = document.createElement("INPUT");
	x.setAttribute("type", "file");
	x.setAttribute("class", "form-control mt-3");
	x.setAttribute("name", "video");
	x.setAttribute("id", "video");
	document.getElementById('video-input').append(x);
}