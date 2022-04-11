var n = 1;

function addVdo() {
	n++;

	var y = document.createElement("INPUT");
	y.setAttribute("class", "form-control mt-3");
	y.setAttribute("type", "text");
	y.setAttribute("name", "videoTitle");
	document.getElementById('videoTitle-input').append(y);

	var x = document.createElement("INPUT");
	x.setAttribute("type", "file");
	x.setAttribute("class", `video-file-${n} form-control mt-3`);
	x.setAttribute("name", "video");
	x.setAttribute("style", "display: block;");
	document.getElementById('video-input').append(x);

	var z = document.createElement("INPUT");
	z.setAttribute("type", "text");
	z.setAttribute("class", `video-url-${n} form-control mt-3`);
	z.setAttribute("name", "videoUrl");
	z.setAttribute("style", "display: none;");
	document.getElementById('video-input').append(z);

	var array = ["ไฟล์","URL"];

	var selectList = document.createElement("SELECT");
	selectList.setAttribute("class", `video-type-${n} form-select mt-3`);
	selectList.setAttribute("onchange", `selectElement(${n})`);
	document.getElementById('video-type').append(selectList);

	for (var i = 0; i < array.length; i++) {
		var option = document.createElement("option");
		option.setAttribute("value", i+1);
		option.text = array[i];
		selectList.appendChild(option);
	}
}