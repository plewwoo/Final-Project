window.onload = setTime;

const url = window.location.href
const vdo = document.getElementById("video")

function setTime () {

    let vdoTitle = vdo.currentSrc
    let curTime = vdo.currentTime
    
    locVdoTitle = localStorage.getItem('vdoTitle', vdoTitle)
    locCurTime = localStorage.getItem('curTime', curTime)
    
    if (vdoTitle == locVdoTitle) {
        vdo.currentTime = locCurTime.toString()
    }
    
}

vdo.addEventListener('pause', function () {

    var vdoTitle = vdo.currentSrc
    var curTime = vdo.currentTime.toFixed(0)

    data = {
        'vdoTitle': vdoTitle,
        'curTime': curTime
    }

    $.ajax({
        type: 'GET',
        url: `${url}save`,
        data: data,
        success: function (response) {
            console.log(response)
            localStorage.setItem('vdoTitle', vdoTitle)
            localStorage.setItem('curTime', curTime)
        },
        error: function (error) {
            console.log(error)
        }
    })
});

vdo.addEventListener('ended', function () {
    console.log('Video ended');

    let ended = {'text': 'Video ended'}

    $.ajax({
        type: 'GET',
        url: `${url}end`,
        data: ended,
        success: function (response) {
            console.log(response)
        },
        error: function (error) {
            console.log(error)
        }
    })
});