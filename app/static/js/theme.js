const switchToggle = document.querySelector('input[type="checkbox"]');
const toggleIcon = document.getElementById('toggle-icon')
const nav = document.getElementById('nav')
const star = document.getElementsByClassName('starPic')

if(localStorage.getItem('darkMode') == 'enabled'){
	document.documentElement.setAttribute('data-theme', 'dark')
	darkMode();
	switchToggle.checked = true
}

function switchMode(e) {
	if(e.target.checked) {
		document.documentElement.setAttribute('data-theme', 'dark')
		localStorage.setItem('darkMode', 'enabled');
		darkMode();
	}

	else {
		document.documentElement.setAttribute('data-theme', 'light')
		localStorage.setItem('darkMode', 'disabled');
		lightMode();
	}
}

function darkMode() {
	toggleIcon.children[0].classList.replace('fa-sun', 'fa-moon')
	nav.style.backgroundColor='#333333'
	for (var i = 0, len = star.length; i < len; i++) {
		star[i].src = '/static/assets/starblack.png'
	}
}

function lightMode() {
	toggleIcon.children[0].classList.replace('fa-moon', 'fa-sun')
	nav.style.backgroundColor='#FFFFFF'
	for (var i = 0, len = star.length; i < len; i++) {
		star[i].src = '/static/assets/starwhite.png'
	}
}

switchToggle.addEventListener('change', switchMode)