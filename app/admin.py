from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

# Register your models here.

admin.site.site_header = 'Media Admin'
admin.site.index_title = 'Main Admin'
admin.site.site_title = 'Media Backend'

admin.site.unregister(Group)

class ProfileAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['profileName', 'major', 'year', 'userType', 'image_tag', 'id']
    list_filter = ['major', 'year', 'userType']

admin.site.register(Profile, ProfileAdmin)

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

class HomeworkInline(admin.TabularInline):
    model = Homework
    extra = 1

class LessonInLine(admin.TabularInline):
    model = Lesson
    extra = 1

class MyCourseInLine(admin.TabularInline):
    model = MyCourse

class OnlineCourseAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['Title', 'courseMajor', 'courseYear', 'courseRating', 'updateDate', 'image_tag', 'active','createBy', 'id']
    list_filter = ['courseMajor', 'courseYear']
    readonly_fields = ['createDate','updateDate']
    fieldsets = (
        (None, {
            'fields': ('courseTitle', ('courseMajor', 'courseYear'), 'createBy', 'active', 'courseHours')
        }),
        ('Advance Options', {
            'classes': ('collapse',),
            'fields': ('courseDesc', 'courseThumbnail', 'courseVideo'),
        }),
        ('Rating & Date', {
            'classes': ('collapse',),
            'fields': ('courseRating', 'courseTaken', 'createDate', 'updateDate'),
        }),
    )
    inlines = [LessonInLine]

admin.site.register(AllCourse, OnlineCourseAdmin)

class LessonAdmin(admin.ModelAdmin):
    list_display = ['course', 'lessonTitle', 'id']
    list_filter = ['course']
    inlines = [VideoInline, HomeworkInline]

admin.site.register(Lesson, LessonAdmin)

class VideoAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['lesson', 'videoTitle']
    list_filter = ['lesson']

admin.site.register(Video, VideoAdmin)

class HomeworkAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['lesson', 'homeworkTitle']
    list_filter = ['lesson']

admin.site.register(Homework, HomeworkAdmin)

class MyCourseAdmin(admin.ModelAdmin):
    ordering = ['user', 'stamp']
    list_display = ['user', 'course', 'image_tag', 'course_id', 'user_id']
    list_filter = ['user', 'course']

admin.site.register(MyCourse, MyCourseAdmin)

admin.site.register(TeacherPending)