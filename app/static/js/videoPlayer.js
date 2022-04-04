const url = window.location.href
const vdo = document.getElementById('video')

vdo.addEventListener('pause', function () {

    var curTime = vdo.currentTime.toFixed(0)

    data = {
        'curTime': curTime
    }

    $.ajax({
        type: 'GET',
        url: `${url}save`,
        data: data,
        success: function (response) {
            console.log('Data from Django : ', response)
        },
        error: function (error) {
            console.log(error)
        }
    })
});

vdo.addEventListener('ended', function () {

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

});