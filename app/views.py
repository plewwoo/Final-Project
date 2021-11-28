from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
import numpy as np
import random

# Create your views here.

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
	user = request.user.profile.id
	course = AllCourse.objects.filter(id = id)
	lesson = Lesson.objects.filter(course = id)
	myCourse = MyCourse.objects.filter(course = id, user = user)
	video = Video.objects.all()
	homework = Homework.objects.filter(course = id)

	lessonCount = lesson.count()
	homeworkCount = homework.count()

	context = {
        'course': course,
		'myCourse' : myCourse,
		'video' : video,
		'lesson' : lesson,
		'homework' : homework,
		'lessonCount' : lessonCount,
		'homeworkCount' : homeworkCount,
		'currentPage' : 'coursePage',
    }

	return render(request, 'app/course.html', context)

def courseQA(request, id):
	course = AllCourse.objects.filter(id = id)

	context = {
        'course': course,
		'currentPage' : 'coursePage',
    }

	return render(request, 'app/qa.html', context)

def myCourse(request, username):
	username = request.user.profile.username
	user = Profile.objects.get(username=username)
	myCourse = MyCourse.objects.filter(user=user)

	context = {
		'course' : myCourse,
		'sidebarTitile' : 'My Course',
		'mycourseActive' : 'active'
	}

	return render(request, 'app/my-course.html', context)

def profile(request, username):
	currentUser = request.user.username
	url = request.GET.get('username', username)
	user = Profile.objects.all()
	
	userId = request.user.profile.id
	allCourse = AllCourse.objects.filter(createBy = userId).order_by('id').reverse()

	labels = []
	data = []

	for course in allCourse:
		labels.append(course.courseTitle)
		data.append(course.courseTaken)
	
	labelCount = len(labels)

	color=["#"+''.join([random.choice('0123456789ABCDEF') for i in range(6)]) for j in range(labelCount)]
	print(color)
	
	context = {
		'currentUser' : currentUser,
		'url' : url,
		'profile' : user,
		'allCourse' : allCourse,
		'labels' : labels,
		'data' : data,
		'color' : color,
		'sidebarTitile' : 'Personal Info',
		'profileActive' : 'active'
	}
	
	return render(request, 'app/profile.html', context)

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
		'sidebarTitile' : 'Personal Info',
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
			return redirect('home-page')
		
		profile.save()
		
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('home-page')

	return render(request, 'app/signup.html')

def addCourse(request):
	userId = request.user.profile.id
	user = Profile.objects.get(id=userId)

	if request.user.profile.userType != 'admin':
		return redirect('home-page')
	
	if request.method == 'POST':
		data = request.POST.copy()
		courseTitle = data.get('courseTitle')
		courseDesc = data.get('courseDesc')
		courseMajor = data.get('courseMajor')
		courseYear = data.get('courseYear')
		lessonTitles = data.getlist('lessonTitle')

		newCourse = AllCourse()
		newCourse.courseTitle = courseTitle
		newCourse.courseDesc = courseDesc
		newCourse.courseMajor = courseMajor
		newCourse.courseYear = courseYear
		newCourse.createBy = user
		file_image = request.FILES['thumbnailImg']
		newCourse.courseThumbnail = file_image
		newCourse.save()

		for lessonTitle in lessonTitles:
			newLesson = Lesson()
			newLesson.course = AllCourse.objects.get(courseTitle=courseTitle)
			newLesson.lessonTitle = lessonTitle
			newLesson.save()

		return redirect('edit-course', newCourse.id)

	context = {
		'sidebarTitile' : 'Add Course',
		'courseMgmtActive' : 'active'
	}

	return render(request, 'app/add-course.html', context)

def courseMgmt (request):
	userId = request.user.profile.id
	course = AllCourse.objects.filter(createBy = userId).order_by('id').reverse()

	context = {
        'course': course,
		'sidebarTitile' : 'Course Management',
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
		lessonTitles = data.getlist('lessonTitle')

		editCourse = AllCourse.objects.get(id=id)
		editCourse.courseTitle = courseTitle
		editCourse.courseDesc = courseDesc
		editCourse.courseMajor = courseMajor
		editCourse.courseYear = courseYear

		for lessonTitle in lessonTitles:
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
		'sidebarTitile' : 'Edit Course',
		'courseMgmtActive' : 'active'
	}

	return render(request, 'app/edit-course.html', context)

def addVdo(request, id, lid):
	cid = request.GET.get('id', id)
	lesson = Lesson.objects.get(id=lid)
	video = Video.objects.filter(lesson_id=lid)
	homework = Homework.objects.filter(lesson_id=lid)

	if request.method == 'POST':
		data = request.POST.copy()
		lessonTitle = data.get('lessonTitle')
		videoTitles = data.getlist('videoTitle')
		videos = request.FILES.getlist('video')
		homeworkTitles = data.getlist('homeworkTitle')
		homeworks = request.FILES.getlist('homework')

		newLesson = Lesson.objects.get(id=lid)
		newLesson.lessonTitle = lessonTitle
		newLesson.save()
		
		for videoTitle, video in zip(videoTitles, videos):
			newVideo = Video()
			newVideo.lesson = Lesson.objects.get(id=lid)
			newVideo.videoTitle = videoTitle
			newVideo.video = video
			newVideo.save()

		for homeworkTitle, homework in zip(homeworkTitles, homeworks):
			newHomework = Homework()
			newHomework.course = AllCourse.objects.get(id = cid)
			newHomework.lesson = Lesson.objects.get(id=lid)
			newHomework.homeworkTitle = homeworkTitle
			newHomework.homework = homework
			newHomework.save()
		
		return redirect('add-vdo', id, lid)

	context = {
		'cid' : cid,
		'lesson' : lesson,
		'homework' : homework,
		'video' : video,
		'sidebarTitile' : 'Add Video',
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

		editVideo.save()
		return redirect('edit-vdo', id, vid)

	context = {
		'cid' : cid,
		'video' : video,
		'sidebarTitile' : 'Edit Video',
		'courseMgmtActive' : 'active'
	}

	return render(request, 'app/edit-vdo.html', context)

def teacherMgmt (request) :
	profile = Profile.objects.filter(userType = 'student')

	context = {
		'profile' : profile,
		'sidebarTitile' : 'Member',
		'teacherMgmtActive' : 'active'
	}

	return render(request, 'app/member-mgmt.html', context)

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