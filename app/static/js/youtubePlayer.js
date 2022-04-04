const url = window.location.href

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var player;
function onYouTubePlayerAPIReady() {
	player = new YT.Player('ytplayer', {
		height: '540',
		width: '960',
		events: {
			'onReady': onPlayerReady,
			'onStateChange': onPlayerStateChange
		}
	});
}

function onPlayerReady(event) {
	player.loadVideoById({
		'videoId': '{{v.videoUrl}}',
		'startSeconds': {{ videoResult.currentTime }}
				});
			}

var done = false;
function onPlayerStateChange(event) {
	console.log('player state change')
	curTime = player.playerInfo.currentTime.toFixed(0);

	console.log(event.data)

	data = {
		'curTime': curTime
	}

	if (event.data == 2) {
		$.ajax({
			type: 'GET',
			url: `${url}save`,
			data: data,
			success: function (response) {
				console.log('Data from Django : ', response)
				localStorage.setItem('username', response.username)
				localStorage.setItem('vdoID', response.vdoID)
				localStorage.setItem('curTime', response.curTime)
			},
			error: function (error) {
				console.log(error)
			}
		})
	}

	if (event.data == 0) {
		console.log('video ended')
		let endedText = 'Video ended'

		data = {
			'endedText': endedText
		}

		$.ajax({
			type: 'GET',
			url: `${url}end`,
			data: data,
			success: function (response) {
				console.log(response)
			},
			error: function (error) {
				console.log(error)
			}
		})
	}
}