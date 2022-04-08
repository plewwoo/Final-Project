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

class QuizInLine(admin.TabularInline):
    model = Quiz
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
    inlines = [VideoInline, QuizInLine]

admin.site.register(Lesson, LessonAdmin)

class VideoAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'lesson', 'videoTitle']
    list_filter = ['lesson']

admin.site.register(Video, VideoAdmin)

class VideoResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'video', 'watched', 'done']
    list_filter = ['user', 'lesson', 'video', 'done']

admin.site.register(VideoResult, VideoResultAdmin)

class MyCourseAdmin(admin.ModelAdmin):
    ordering = ['user', 'stamp']
    list_display = ['user', 'course', 'image_tag', 'course_id', 'user_id']
    list_filter = ['user', 'course']

admin.site.register(MyCourse, MyCourseAdmin)

admin.site.register(TeacherPending)

admin.site.register(Comment)

admin.site.register(Review)

admin.site.register(Result)

admin.site.register(Quiz)

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['id', 'text']

admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text', 'correct']

admin.site.register(Answer, AnswerAdmin)