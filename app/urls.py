import imp


import tkinter
from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
	path('', index, name='home-page'),
	path('online-course', onlineCourse, name='online-course'),
	path('course/<int:id>', course, name='course'),
	path('profile/<str:username>/', profile, name='profile-page'),
	path('profile/<str:username>/edit/', editProfile, name='editProfile-page'),
	path('profile/<str:username>/course/', myCourse, name='my-course'),
	path('signup', signUp, name='signin-page'),
	path('add-course', addCourse, name='add-course'),
	path('edit-course/<int:id>/', editCourse, name='edit-course'),
	path('edit-course/<int:id>/edit-lesson/<int:lid>/', editLesson, name='edit-lesson'),
	path('edit-course/<int:id>/delete-lesson/<int:lid>/', deleteLesson, name='delete-lesson'),
	path('edit-course/<int:id>/edit-vdo/<int:vid>/', editVideo, name='edit-vdo'),
	path('edit-course/<int:id>/delete-vdo/<int:vid>/', deleteVideo, name='delete-vdo'),
	path('edit-course/<int:id>/edit-quiz/<int:qid>/', editQuiz, name='edit-quiz'),
	path('edit-course/<int:id>/delete-quiz/<int:qid>/', deleteQuiz, name='delete-quiz'),
	path('edit-course/<int:id>/edit-question/<int:qid>/', editQuestion, name='edit-question'),
	path('take-course/<int:id>', addMycourse, name='take-course'),
	path('course-management', courseMgmt, name='course-management'),
	path('update-course-status/<int:id>/<str:status>', updateCourseStatus, name='updateCourseStatus'),
	path('member', member, name='member'),
	path('teacher', teacher, name='teacher'),
	path('teacher-register', teacherRegister, name='teacher-register'),
	path('update-teacher-status/<int:uid>/<int:tid>/<str:status>', updateTeacherStatus, name='updateTeacherStatus'),
	path('video/<int:id>', video, name="video"),
	path('video/<int:id>/<int:vid>/', videoPlayer, name="videoPlayer"),
	path('video/<int:id>/<int:vid>/save', videoSave, name="videoSave"),
	path('video/<int:id>/<int:vid>/end', videoEnd, name="videoEnd"),
	path('quiz/', QuizListView.as_view(), name='quiz-main'),
	path('quiz/<pk>/', quiz_view, name='quiz-view'),
	path('quiz/<pk>/save/', save_quiz_view, name='save-data-view'),
	path('quiz/<pk>/data/', quiz_data_view, name='quiz-data-view'),
]