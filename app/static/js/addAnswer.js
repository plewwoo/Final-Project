const answerContainer = document.getElementById('answer-container')

function addAnswer() {
	answerContainer.insertAdjacentHTML('beforeend', `
	<div class="answer d-flex justify-content-between align-items-center mt-3">
		<div class="col-sm-8 pl-0">
			<input type="text" class="form-control" name="answer">
		</div>
		<div class="col-sm-4 d-flex justify-content-between align-items-center">
			<div class="pl-3">
				<input class="form-check-input" type="checkbox" name="correct" value="on">
				<label class="form-label m-0 pl-2">ถูก</label>
			</div>
			<div>
				<input class="form-check-input" type="checkbox" name="correct" value="off">
				<label class="form-label m-0 pl-2">ผิด</label>
			</div>
		</div>
	</div>
	`)
}