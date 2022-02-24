function selectElement(n) {
	let videoFile = document.getElementsByClassName(`video-file-${n}`)
	let videoUrl = document.getElementsByClassName(`video-url-${n}`)

	const selectType  = document.querySelector(`.video-type-${n}`).value;

		if (selectType == 1){
			for (var i = 0, len = videoFile.length; i < len; i++) {
				videoFile[i].style.display = "block";
			}
			for (var i = 0, len = videoUrl.length; i < len; i++) {
				videoUrl[i].style.display = "none";
			}
			console.log(selectType)
		}
		else {
			for (var i = 0, len = videoFile.length; i < len; i++) {
				videoFile[i].style.display = "none";
			}
			for (var i = 0, len = videoUrl.length; i < len; i++) {
				videoUrl[i].style.display = "block";
			}
			console.log(selectType)
		}
}