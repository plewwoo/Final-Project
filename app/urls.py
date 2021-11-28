from django.urls import path
from .views import *

urlpatterns = [
	path('', index, name='home-page'),
	path('online-course', onlineCourse, name='online-course'),
	path('course/<int:id>', course, name='course'),
	path('course/<int:id>/Q&A', courseQA, name='course-qa'),
	path('profile/<str:username>/', profile, name='profile-page'),
	path('profile/<str:username>/edit/', editProfile, name='editProfile-page'),
	path('profile/<str:username>/course/', myCourse, name='my-course'),
	path('signup', signUp, name='signin-page'),
	path('add-course', addCourse, name='add-course'),
	path('edit-course/<int:id>/', editCourse, name='edit-course'),
	path('edit-course/<int:id>/add-vdo/<int:lid>/', addVdo, name='add-vdo'),
	path('edit-course/<int:id>/edit-vdo/<int:vid>/', editVideo, name='edit-vdo'),
	path('take-course/<int:id>', addMycourse, name='take-course'),
	path('course-management', courseMgmt, name='course-management'),
	path('update-course-status/<int:id>/<str:status>', updateCourseStatus, name='updateCourseStatus'),
	path('member-management', teacherMgmt, name='member-management'),
]