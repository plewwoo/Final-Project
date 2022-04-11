const url = window.location.href
const vdo = document.getElementById('video')

vdo.addEventListener('pause', function () {

    const cid_ = JSON.parse(document.getElementById('cid').textContent);
    const vid = JSON.parse(document.getElementById('vid').textContent);
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
            localStorage.setItem('latestCourse', cid_)
			localStorage.setItem('latestVdo', vid)
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