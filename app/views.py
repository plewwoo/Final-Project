import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Avg
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import *

def index(request):
	allCourse = AllCourse.objects.all().order_by('id').reverse()
	paginator = Paginator(allCourse, 3)
	course = paginator.get_page(paginator)

	context = {
        'allCourse': course,
		'currentPage' : 'index',
    }
	
	return render(request, 'app/index.html', context)

def onlineCourse(request):
	allCourse = AllCourse.objects.all().order_by('id').reverse()

	context = {
        'allCourse': allCourse,
    }

	return render(request, 'app/online-course.html', context)

def course(request, id):
	try:
		userId = request.user.profile.id
		user = Profile.objects.get(id=userId)
		course = AllCourse.objects.get(id = id)
		
		if request.method == 'POST':
			data = request.POST.copy()
			rating = data.get('rating')
			review = data.get('review')
			comment = data.get('qa')

			if data.get('rating') and ('reveiw') if 'rating' and 'review' in request.POST else None:
				newReview = Review()
				newReview.user = user
				newReview.rating = rating
				newReview.review = review
				newReview.course = course
				newReview.save()


			if data.get('qa') if 'qa' in request.POST else None:
				newComment = Comment()
				newComment.user = user
				newComment.comment = comment
				newComment.course = course
				newComment.save()
				
			return redirect('course', id)

		user = request.user.profile.id
		course = AllCourse.objects.filter(id = id)
		lesson = Lesson.objects.filter(course = id)
		myCourse = MyCourse.objects.filter(course = id, user = user)
		video = Video.objects.all()
		comment = Comment.objects.filter(course=id)
		review = Review.objects.filter(course = id)
		avgRating = Review.objects.filter(course = id).aggregate(Avg('rating'))

		quizes = []

		for l in lesson:
			quiz = Quiz.objects.filter(lesson = l)
			if quiz.exists():
				quizes.extend(quiz)
	
		quizCount = len(quizes)
		lessonCount = lesson.count()
	except:
		course = AllCourse.objects.filter(id = id)
		lesson = Lesson.objects.filter(course = id)
		myCourse = MyCourse.objects.filter(course = id)
		video = Video.objects.all()
		quiz = Quiz.objects.all()
		comment = Comment.objects.filter(course=id)
		review = Review.objects.filter(course = id)
		avgRating = Review.objects.filter(course = id).aggregate(Avg('rating'))

		quizes = []

		for l in lesson:
			quiz = Quiz.objects.filter(lesson = l)
			if quiz.exists():
				quizes.extend(quiz)
	
		quizCount = len(quizes)
		lessonCount = lesson.count()

	newCourse = AllCourse.objects.get(id = id)
	avg = avgRating.get('rating__avg')
	newCourse.courseRating = avg
	newCourse.save()

	context = {
        'course': course,
		'myCourse' : myCourse,
		'video' : video,
		'lesson' : lesson,
		'comment' : comment,
		'review' : review,
		'lessonCount' : lessonCount,
		'quizCount': quizCount,
		'currentPage' : 'coursePage',
    }

	return render(request, 'app/course.html', context)

def myCourse(request, username):
	username = request.user.profile.username
	user = Profile.objects.get(username=username)
	myCourse = MyCourse.objects.filter(user=user)

	context = {
		'course' : myCourse,
		'sidebarTitile' : 'คอร์สของฉัน',
		'mycourseActive' : 'active'
	}

	return render(request, 'app/my-course.html', context)

@login_required
def profile(request, username):
	currentUser = request.user.username
	url = request.GET.get('username', username)
	user = Profile.objects.filter(username = username)

	userId = request.user.profile.id
	allCourse = AllCourse.objects.filter(createBy = userId).order_by('id').reverse()

	teacher = TeacherPending.objects.all()
	labels = []
	data = []

	for course in allCourse:
		labels.append(course.courseTitle)
		data.append(course.courseTaken)
	
	context = {
		'currentUser' : currentUser,
		'url' : url,
		'profile' : user,
		'teacher' : teacher,
		'allCourse' : allCourse,
		'labels' : labels,
		'data' : data,
		'sidebarTitile' : 'ข้อมูลส่วนตัว',
		'profileActive' : 'active'
	}
	
	return render(request, 'app/profile.html', context)

def courseDetail (request, username):
	currentUser = request.user.username
	url = request.GET.get('username', username)
	user = Profile.objects.filter(username = username)

	userId = request.user.profile.id
	allCourse = AllCourse.objects.filter(createBy = userId)

	print('cid', allCourse)

	lessons = []
	myCourses = []

	for a in allCourse:
		myCourse = MyCourse.objects.filter(course=a)
		myCourses.extend(myCourse)
		lesson = Lesson.objects.filter(course = a).values_list('id', flat=True)
		lessons.extend(lesson)
	
	print(myCourses)
	print(lessons)
		
	videos_ = []
	quizes_ = []

	for l in lessons:
		video = Video.objects.filter(lesson = l).values_list('id', flat=True)
		videos= list(video)
		videos_.extend(videos)
		print('Videos : ', videos)
		quiz_ = Quiz.objects.filter(lesson = l).values_list('id', flat=True)
		quizes= list(quiz_)
		quizes_.extend(quizes)
		print('quizes_ : ', quizes_)

	numVideo = len(videos_)
	numQuiz = len(quizes_)

	context = {
		'currentUser' : currentUser,
		'url' : url,
		'profile' : user,
		'allCourse' : allCourse,
		'myCourse': myCourses,
		'numVideo': numVideo,
		'numQuiz': numQuiz,
		'sidebarTitile' : 'รายละเอียดคอร์ส',
		'courseDetailActive' : 'active'
	}

	return render(request, 'app/course-detail.html', context)

def courseDetail2 (request, username):
	currentUser = request.user.username
	url = request.GET.get('username', username)
	user = Profile.objects.filter(username = username)

	userId = request.user.profile.id
	allCourse = AllCourse.objects.filter(createBy = userId)

	myCourses = []

	for a in allCourse:
		myCourse = MyCourse.objects.filter(course=a)
		myCourses.extend(myCourse)
		
	print(myCourses)

	context = {
		'currentUser' : currentUser,
		'url' : url,
		'profile' : user,
		'allCourse' : allCourse,
		'myCourse': myCourses,
		'sidebarTitile' : 'รายละเอียดคอร์ส',
		'courseDetailActive' : 'active'
	}

	return render(request, 'app/course-detail.html', context)

def editProfile(request, username):
	username = request.user.username
	user = User.objects.get(username=username)

	if request.method == 'POST' :
		data = request.POST.copy()
		firstName = data.get('first-name')
		lastName = data.get('last-name')
		email = data.get('email')
		tel = data.get('tel')

		editUser = User.objects.get(username = user)
		editUser.first_name = firstName
		editUser.last_name = lastName
		editUser.email = email
		editUser.save()

		newProfile = Profile.objects.get(user=user)
		newProfile.tel = tel

		if request.FILES['editProfilePic'] if 'editProfilePic' in request.FILES else None:
			file_image = request.FILES['editProfilePic'] 
			newProfile.photo = file_image
			newProfile.save()
			return redirect('profile-page', username)

		newProfile.save()
		return redirect('profile-page', username)
	
	profile = Profile.objects.filter(user=user)
	
	context = {
		'profile' : profile,
		'sidebarTitile' : 'ข้อมูลส่วนตัว',
		'profileActive' : 'active'
	}

	return render(request, 'app/edit-profile.html', context)

def signUp(request):

	if request.method == 'POST':
		data = request.POST.copy()
		username = data.get('username')
		firstName = data.get('first-name')
		lastName = data.get('last-name')
		email = data.get('email')
		tel = data.get('tel')
		major = data.get('major')
		year = data.get('year')
		password = data.get('password')

		newUser = User()
		newUser.username = username
		newUser.email = email
		newUser.first_name = firstName
		newUser.last_name = lastName
		newUser.set_password(password)
		newUser.save()

		profile = Profile()
		profile.user = User.objects.get(username=username)
		profile.username = username
		profile.tel = tel
		profile.major = major
		profile.year = year

		if request.FILES['profilePicUpload'] if 'profilePicUpload' in request.FILES else None:
			file_image = request.FILES['profilePicUpload']
			profile.photo = file_image
			profile.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('home-page')
		
		profile.save()
		
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('home-page')

	return render(request, 'app/signup.html')

def addCourse(request):
	userId = request.user.profile.id
	user = Profile.objects.get(id=userId)

	if request.user.profile.userType != 'admin' and request.user.profile.userType != 'teacher':
		return redirect('home-page')
	
	
	if request.method == 'POST':
		data = request.POST.copy()
		courseTitle = data.get('courseTitle')
		courseDesc = data.get('courseDesc')
		courseMajor = data.get('courseMajor')
		courseYear = data.get('courseYear')
		courseHours = data.get('courseHours')
		lessonTitles = data.getlist('lessonTitle')

		newCourse = AllCourse()
		newCourse.courseTitle = courseTitle
		newCourse.courseDesc = courseDesc
		newCourse.courseMajor = courseMajor
		newCourse.courseYear = courseYear
		newCourse.createBy = user
		newCourse.courseHours = courseHours
		file_image = request.FILES['thumbnailImg']
		newCourse.courseThumbnail = file_image
		newCourse.save()

		for lessonTitle in lessonTitles:
			if lessonTitle != '':
				newLesson = Lesson()
				newLesson.course = AllCourse.objects.get(courseTitle=courseTitle)
				newLesson.lessonTitle = lessonTitle
				newLesson.save()

		return redirect('edit-course', newCourse.id)

	context = {
		'sidebarTitile' : 'เพิ่มคอร์สเรียน',
		'courseMgmtActive' : 'active'
	}

	return render(request, 'app/add-course.html', context)

def courseMgmt (request):
	userId = request.user.profile.id

	if request.user.profile.userType == 'admin':
		course = AllCourse.objects.all().order_by('id').reverse()
	elif request.user.profile.userType == 'teacher':
		course = AllCourse.objects.filter(createBy=userId).order_by('id').reverse()

	context = {
        'course': course,
		'sidebarTitile' : 'จัดการคอร์สเรียน',
		'courseMgmtActive' : 'active'
    }

	return render(request, 'app/course-mgmt.html', context)

def updateCourseStatus (request, id, status):
	if request.user.profile.userType != 'admin':
		return redirect('home-page')

	course = AllCourse.objects.get(id=id)
	if status == 'active':
		course.active = True
	elif status == 'inactive':
		course.active = False
	course.save()
	
	return redirect ('course-management')

def editCourse (request, id) :
	course = AllCourse.objects.get(id=id)
	lesson = Lesson.objects.filter(course=id)

	if request.method == 'POST':
		data = request.POST.copy()
		courseTitle = data.get('courseTitle')
		courseDesc = data.get('courseDesc')
		courseMajor = data.get('courseMajor')
		courseYear = data.get('courseYear')
		courseHours = data.get('courseHours')
		lessonTitles = data.getlist('lessonTitle')

		editCourse = AllCourse.objects.get(id=id)
		editCourse.courseTitle = courseTitle
		editCourse.courseDesc = courseDesc
		editCourse.courseMajor = courseMajor
		editCourse.courseYear = courseYear
		editCourse.courseHours = courseHours

		
		for lessonTitle in lessonTitles:
			if lessonTitle != '':
				newLesson = Lesson()
				newLesson.course = AllCourse.objects.get(courseTitle=courseTitle)
				newLesson.lessonTitle = lessonTitle
				newLesson.save()
		
		if request.FILES['thumbnailImg'] if 'thumbnailImg' in request.FILES else None:
			file_image = request.FILES['thumbnailImg']
			editCourse.courseThumbnail = file_image
			editCourse.save()
			return redirect('edit-course', id)

		editCourse.save()

		return redirect('edit-course', id)

	context = {
		'course' : course,
		'lesson' : lesson,
		'sidebarTitile' : 'จัดการคอร์สเรียน',
		'courseMgmtActive' : 'active'
	}

	return render(request, 'app/edit-course.html', context)

def deleteLesson(request, id, lid):
	cid = request.GET.get('id', id)
	lesson = Lesson.objects.get(id=lid)
	lesson.delete()

	return redirect('edit-course', cid)
	
def editLesson(request, id, lid):
	cid = request.GET.get('id', id)
	lesson = Lesson.objects.get(id=lid)
	video = Video.objects.filter(lesson_id=lid)
	quiz = Quiz.objects.filter(lesson_id=lid)

	if request.method == 'POST':
		data = request.POST.copy()
		lessonTitle = data.get('lessonTitle')
		videoTitles = data.getlist('videoTitle')
		videos = request.FILES.getlist('video')
		videosUrl = data.getlist('videoUrl')
		quizTitle = data.get('quizTitle')
		quizTopic = data.get('quizTopic')
		numQuestions = data.get('numQuestions')
		quizTime = data.get('quizTime')
		requiredScore = data.get('requiredScore')
		difficulty = data.get('difficulty')

		newLesson = Lesson.objects.get(id=lid)
		newLesson.lessonTitle = lessonTitle
		newLesson.save()

		if videos:
			for videoTitle, video in zip(videoTitles, videos):
				if videoTitle != "":
					newVideo = Video()
					newVideo.lesson = Lesson.objects.get(id=lid)
					newVideo.videoTitle = videoTitle
					newVideo.video = video
					newVideo.save()
					print('video',videos)

		elif videosUrl:
			for videoTitle, videoUrl in zip(videoTitles, videosUrl):
				if videoTitle != "":
					newVideo = Video()
					newVideo.lesson = Lesson.objects.get(id=lid)
					newVideo.videoTitle = videoTitle
					x = videoUrl.split('=')
					y = x[1].split('&')
					newVideo.videoUrl = y[0]
					newVideo.save()
					print('videourl',videosUrl)
		
		if quizTitle:
			newQuiz = Quiz()
			newQuiz.name = quizTitle
			newQuiz.topic = quizTopic
			newQuiz.lesson = Lesson.objects.get(id=lid)
			newQuiz.numberOfQuestions = numQuestions
			newQuiz.time = quizTime
			x = requiredScore.split('%')
			newQuiz.requiredScore = x[0]
			newQuiz.difficulty = difficulty
			newQuiz.save()
		
		return redirect('edit-lesson', id, lid)

	context = {
		'cid' : cid,
		'lesson' : lesson,
		'quiz' : quiz,
		'video' : video,
		'sidebarTitile' : 'เพิ่มวิดีโอ & แบบฝึกหัด',
		'courseMgmtActive' : 'active'
	}

	return render (request, 'app/add-vdo.html', context)

def editVideo(request, id, vid):
	cid = request.GET.get('id', id)
	video = Video.objects.filter(id = vid)

	if request.method == 'POST':
		data = request.POST.copy()
		videoTitle = data.get('videoTitle')

		editVideo = Video.objects.get(id=vid)
		editVideo.videoTitle = videoTitle

		if request.FILES['video'] if 'video' in request.FILES else None:
			video = request.FILES['video']
			editVideo.video = video
			editVideo.save()
			return redirect('edit-vdo', id, vid)
		
		if data.get('videoUrl') if 'videoUrl' in request.POST else None:
			videoUrl = data.get('videoUrl')
			x = videoUrl.split('=')
			y = x[1].split('&')
			editVideo.videoUrl = y[0]
			editVideo.save()
			return redirect('edit-vdo', id, vid)

		editVideo.save()
		return redirect('edit-vdo', id, vid)

	context = {
		'cid' : cid,
		'video' : video,
		'sidebarTitile' : 'แก้ไขวิดีโอ',
		'courseMgmtActive' : 'active'
	}

	return render(request, 'app/edit-vdo.html', context)

def deleteVideo(request, id, vid):
	cid = request.GET.get('id', id)
	video = Video.objects.filter(id = vid)
	videoLesson = Video.objects.filter(id = vid).values_list('lesson', flat=True)
	lid = videoLesson[0]
	video.delete()

	return redirect('edit-lesson', cid, lid)

def editQuiz(request, id, qid):
	cid = request.GET.get('id', id)
	quiz = Quiz.objects.filter(id = qid)
	question = Question.objects.filter(quiz = qid)

	if request.method == 'POST' :
		data = request.POST.copy()
		quizTitle = data.get('quizTitle')
		quizTopic = data.get('quizTopic')
		numQuestions = data.get('numQuestions')
		quizTime = data.get('quizTime')
		requiredScore = data.get('requiredScore')[:2]
		difficulty = data.get('difficulty')
		
		question = data.get('question')
		answers = data.getlist('answer')
		corrects = data.getlist('correct')

		editQuiz = Quiz.objects.get(id = qid)
		editQuiz.name = quizTitle
		editQuiz.topic = quizTopic
		editQuiz.numberOfQuestions = numQuestions
		editQuiz.time = quizTime
		x = requiredScore.split('%')
		editQuiz.requiredScore = x[0]
		editQuiz.difficulty = difficulty
		editQuiz.save()

		questionId = None

		if question:
			newQuestion = Question()
			newQuestion.text = question
			newQuestion.quiz = Quiz.objects.get(id = qid)
			newQuestion.save()
			questionId = newQuestion.id
			print('Question ID :', questionId)

			for answer, correct in zip(answers, corrects):
				newAnswer = Answer()
				newAnswer.text = answer
				if correct == 'on':
					newAnswer.correct = True
				else :
					newAnswer.correct = False
				newAnswer.question = Question.objects.get(id = questionId)
				newAnswer.save()
		
		return redirect('edit-quiz', id, qid)

	context = {
		'cid' : cid,
		'quiz' : quiz,
		'question' : question,
		'sidebarTitile' : 'จัดการแบบฝึกหัด',
		'courseMgmtActive' : 'active'
	}

	return render(request, 'app/edit-quiz.html', context)

def deleteQuiz(request, id, qid):
	cid = request.GET.get('id', id)
	quiz = Quiz.objects.filter(id = qid)
	quizLesson = Quiz.objects.filter(id = qid).values_list('lesson', flat=True)
	lid = quizLesson[0]
	quiz.delete()

	return redirect('edit-lesson', cid, lid)

def editQuestion (request, id, qid) :
	cid = request.GET.get('id', id)
	question = Question.objects.filter(quiz = qid)
	answer = Answer.objects.filter(question = qid)

	if request.method == 'POST' :
		data = request.POST.copy()
		question = data.get('question')
		answersId = data.getlist('answerId')
		answers = data.getlist('answer')
		corrects = data.getlist('correct')
		print(data)

		if question :
			editQuestion = Question.objects.get(id = qid)
			editQuestion.text = question
			editQuestion.save()

		answer = []
		
		for aid, a, c in zip(answersId, answers, corrects) :
			dt = [aid, a, c]
			answer.append(dt)
			print(answer)
		
		for ans in answer :
			editAnswer = Answer.objects.get(id = ans[0])
			editAnswer.text = ans[1]
			if ans[2] == 'on':
				editAnswer.correct = True
			else :
				editAnswer.correct = False
			editAnswer.save()
		
		return redirect('edit-question', id, qid)

	context = {
		'cid' : cid,
		'qid' : qid,
		'question' : question,
		'answer' : answer,
		'sidebarTitile' : 'แก้ไขคำถาม',
		'courseMgmtActive' : 'active'
	}

	return render(request, 'app/edit-question.html', context)

def member (request) :
	profile = Profile.objects.filter(userType__in = ['student','teacher'])

	context = {
		'profile' : profile,
		'sidebarTitile' : 'สมาชิก',
		'memberActive' : 'active'
	}

	return render(request, 'app/member-mgmt.html', context)

def teacher (request) :
	teacher = TeacherPending.objects.all()

	context = {
		'teacher' : teacher,
		'sidebarTitile' : 'อาจารย์',
		'teacherActive' : 'active'
	}

	return render(request, 'app/teacher-mgmt.html', context)

def updateTeacherStatus (request, uid, tid, status):
	if request.user.profile.userType != 'admin':
		return redirect('home-page')

	teacherPending = TeacherPending.objects.get(id=tid)
	profile = Profile.objects.get(id=uid)
	
	if status == 'approve':
		teacherPending.approve = True
		profile.userType = 'teacher'
		teacherPending.save()
	elif status == 'disapprove':
		teacherPending.approve = False
		profile.userType = 'student'
		profile.apply = False
		teacherPending.delete()

	profile.save()
	
	return redirect ('teacher')

def teacherRegister (request):
	username = request.user.profile.username
	user = Profile.objects.get(username=username)

	if request.method == 'POST':
		data = request.POST.copy()
		interest = data.get('interest')
		work = data.get('work')
		portfolio = data.get('portfolio')

		newTeacher = TeacherPending()
		newTeacher.user = user
		newTeacher.interest = interest
		newTeacher.work = work
		newTeacher.portfolio = portfolio
		newTeacher.save()

		user = Profile.objects.get(username=username)
		user.apply = True
		user.save()

		return redirect ('profile-page', username)

	context = {
		'sidebarTitile' : 'สมัครเป็นอาจารย์',
		'profileActive' : 'active'
	}

	return render(request, 'app/teacher-register.html', context)

def addMycourse (request, id):
	username = request.user.profile.username
	user = Profile.objects.get(username=username)
	course = AllCourse.objects.get(id=id)

	if MyCourse.objects.filter(user=user, courseId=id):
		pass
	else:
		newCourse = MyCourse()
		newCourse.user = user
		newCourse.courseId = id
		newCourse.course = course
		newCourse.save()
		courseAdd = AllCourse.objects.get(id=id)
		courseCount = courseAdd.courseTaken + 1
		courseAdd.courseTaken = courseCount
		courseAdd.save()

	return redirect('my-course', 'username')

@login_required
def video (request, id):
	cid = request.GET.get('id', id)
	course = AllCourse.objects.filter(id = id)
	lesson = Lesson.objects.filter(course = id)
	lessonId = Lesson.objects.filter(course = id).values_list('id', flat=True)
	lessonList = list(lessonId)
	video = Video.objects.all()
	quiz = Quiz.objects.filter(lesson = lessonList[0])


	context = {
		'cid' : cid,
		'course' : course,
		'lesson' : lesson,
		'video' : video,
		'quiz' : quiz,
	}

	return render(request,'app/video.html', context)

@login_required
def videoPlayer (request, id, vid):
	cid = request.GET.get('id', id)
	vid = request.GET.get('vid', vid)
	username = request.user.profile.username
	user = Profile.objects.get(username=username)
	course = AllCourse.objects.get(id = id)
	lesson = Lesson.objects.filter(course = id)
	lessonId = Lesson.objects.filter(course = id).values_list('id', flat=True)
	lessonList = list(lessonId)
	video = Video.objects.all()
	videoLesson = Video.objects.get(id = vid)

	if MyCourse.objects.filter(user=user, course=course) or request.user.profile.userType == 'admin' or request.user.profile.userType == 'teacher':
		pass
	else:
		return redirect('course', cid)

	if VideoResult.objects.filter(user = user, course = id, lesson = videoLesson.lesson, video = videoLesson) :
		pass
	else :
		VideoResult.objects.create(user = user, course = course, lesson = videoLesson.lesson, video = videoLesson, watched = True)

	videoResult = VideoResult.objects.filter(user = user, video = vid)
	quiz = Quiz.objects.filter(lesson = lessonList[0])

	context = {
		'cid' : cid,
		'vid' : vid,
		'course' : course,
		'lesson' : lesson,
		'video' : video,
		'videoResult': videoResult,
		'quiz' : quiz,
	}

	return render(request,'app/videoplayer.html', context)

def videoSave (request, id, vid):
	vid = request.GET.get('vid', vid)
	username = request.user.profile.username
	user = Profile.objects.get(username=username)

	videoLesson = Video.objects.get(id = vid)

	curTime = request.GET.get('curTime')

	print('Current Time :', curTime)

	if request.is_ajax() :
		editVideoResult = VideoResult.objects.get(user = user, course = id, lesson = videoLesson.lesson, video = videoLesson)
		editVideoResult.currentTime = curTime
		editVideoResult.save()

	return JsonResponse({
		'username': username,
		'vdoID': vid,
		'curTime': curTime
	})

def videoEnd(request, id, vid) :
	cid = request.GET.get('id', id)
	vid = request.GET.get('vid', vid)
	username = request.user.profile.username
	user = Profile.objects.get(username=username)
	course = AllCourse.objects.get(id = cid)
	lesson = Lesson.objects.filter(course = course.id)
	lessonID = Lesson.objects.filter(course = course.id).values_list('id', flat=True)
	lessonList = list(lessonID)
	print('Course ID :', course.id)
	print('Lesson :', lesson)
	print('Lesson ID :', lessonID)
	print('Lesson List :', lessonList)
	
	videoLesson = Video.objects.get(id = vid)
	print('video lesson : ', videoLesson.lesson)

	videos_ = []
	
	for l in lessonList:
		video = Video.objects.filter(lesson = l).values_list('id', flat=True)
		videos= list(video)
		videos_.extend(videos)
		print('Videos : ', videos)
	
	if Result.objects.filter(user = user, course = id, lesson = videoLesson.lesson, video = videoLesson, done = True) :
		pass
	else :
		editvideoResult = VideoResult.objects.get(user = user, course = course, lesson = videoLesson.lesson, video = videoLesson, watched = True, done = False)
		editvideoResult.done = True
		editvideoResult.save()
		
	print('Number of Videos : ', videos_)
	print('Number of Videos : ', len(videos_))

	numVideo = len(videos_)
	
	multiplier = 100 / numVideo

	if request.is_ajax() :
		editCourse = MyCourse.objects.get(course = id, user = user)
		if editCourse.numVideo <= numVideo :
			endVideo = VideoResult.objects.filter(user = user, course = course, done = True).count()
			print('end Video : ' ,endVideo)
			editCourse.numVideo = endVideo
			videoPercentage = endVideo * multiplier
		elif editCourse.numVideo >= numVideo :
			editCourse.numVideo = numVideo
			videoPercentage = 100
		editCourse.progress = videoPercentage
		print(videoPercentage)
		editCourse.save()

	text = request.GET.get('endedText')

	return JsonResponse({
		'text': text
	})

################# Quiz #################

class QuizListView(ListView):
	model = Quiz
	template_name = 'app/quizMain.html'

def quiz_view(request, id, pk):
	cid = request.GET.get('id', id)

	quiz = Quiz.objects.get(pk = pk)

	context = {
		'quiz': quiz
	}

	return render(request, 'app/quiz.html', context)

def quiz_data_view(request, id, pk):
	quiz = Quiz.objects.get(pk = pk)
	questions = []
	for q in quiz.get_questions():
		answers = []
		for a in q.get_answers():
			answers.append(a.text)
		questions.append({str(q): answers})

	return JsonResponse({
		'data': questions,
		'time': quiz.time,
	})

def save_quiz_view(request, id, pk):
	if request.is_ajax():
		questions = []
		data = request.POST
		data_ = dict(data.lists())

		data_.pop('csrfmiddlewaretoken')

		for k in data_.keys():
			print('key', k)
			question = Question.objects.get(text=k)
			questions.append(question)
		print(questions)	
		
		username = request.user.profile.username
		user = Profile.objects.get(username=username)
		quiz = Quiz.objects.get(pk = pk)
		
		score = 0
		multiplier = 100 / quiz.numberOfQuestions
		results = []
		correctAnswer = None

		for q in questions:
			a_selected = request.POST.get(q.text)
			
			if a_selected != "":
				question_answers = Answer.objects.filter(question=q)
				for a in question_answers:
					if a_selected == a.text:
						if a.correct:
							score += 1
							correctAnswer = a.text
					else :
						if a.correct:
							correctAnswer = a.text
				results.append({str(q): {'correctAnswer': correctAnswer, 'answered': a_selected}})
			else :
				results.append({str(q): 'not answered'})
		
		lastScore = score * multiplier

		cid = request.GET.get('id', id)
		course = AllCourse.objects.get(id = cid)
		lesson = Lesson.objects.filter(course = course.id)
		lessonID = Lesson.objects.filter(course = course.id).values_list('id', flat=True)
		lessonList = list(lessonID)

		quizLesson = Quiz.objects.get(id = pk)

		quizes_ = []
	
		for l in lessonList:
			quiz_ = Quiz.objects.filter(lesson = l).values_list('id', flat=True)
			quizes= list(quiz_)
			quizes_.extend(quizes)
			print('quizes_ : ', quizes_)

		numQuiz = len(quizes_)
		
		if lastScore >= quiz.requiredScore:
			if Result.objects.filter(quiz=quiz, user=user):
				pass
			else:
				Result.objects.create(course=course, lesson=quizLesson.lesson, quiz=quiz, user=user, score=lastScore, done=True, passed=True)

				editCourse = MyCourse.objects.get(course = id, user = user)
				if editCourse.passedQuiz <= numQuiz :
					passedQuiz = Result.objects.filter(user = user, course = course, done = True, passed=True).count()
					print('passedQuiz : ' ,passedQuiz)
					editCourse.passedQuiz = passedQuiz
					editCourse.save()

			return JsonResponse({'passed': True, 'score': lastScore, 'results': results})
		else:
			if Result.objects.filter(quiz=quiz, user=user):
				pass
			else:
				Result.objects.create(course=course, lesson=quizLesson.lesson, quiz=quiz, user=user, score=lastScore, done=True, passed=False)
			return JsonResponse({'passed': False, 'score': lastScore, 'results': results})
