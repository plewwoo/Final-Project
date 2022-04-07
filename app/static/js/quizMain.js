const modalBtns = [...document.getElementsByClassName('modalbtn')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')
const cid = JSON.parse(document.getElementById('cid').textContent);

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
	const pk = modalBtn.getAttribute('data-pk')
	const name = modalBtn.getAttribute('data-quiz')
	const numQuestions = modalBtn.getAttribute('data-question')
	const difficulty = modalBtn.getAttribute('data-difficult')
	const scoreToPass = modalBtn.getAttribute('data-pass')
	const time = modalBtn.getAttribute('data-time')

	modalBody.innerHTML = `
	<div class="h5 mb-3">คุณแน่ใจหรือว่าต้องการเริ่มทำแบบฝึกหัด "<b>${name}</b>"?</div>
	<div class="text-muted">
		<ul>
			<li>ระดับความยาก : <b>${difficulty}</b></li>
			<li>จำนวนคำถาม : <b>${numQuestions}</b></li>
			<li>เกณฑ์การผ่าน : <b>${scoreToPass}%</b></li>
			<li>เวลาที่จำกัด : <b>${time} นาที</b></li>
		</ul>
	</div>
	`

	startBtn.setAttribute('href', `/quiz/${cid}/${pk}`)
}))