from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.html import mark_safe
from django.db.models import Count
from ckeditor.fields import RichTextField

# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to="profilePic/", null=True, blank=True)
    tel = models.CharField(max_length=12, null=True, blank=True)
    major = models.CharField(max_length=100,null=True, blank=True, choices=[('Digital Media Technology', 'Digital Media Technology'), ('Game Development', 'Game Development'), ('Medical Media Innovation', 'Medical Media Innovation')])
    year = models.IntegerField(null=True, blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])
    userType = models.CharField(max_length=100, default="student", choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')])
    
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def profileName(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    
    profileName.short_description = 'Name'
    
    def image_tag(self):
        if self.photo:
            return mark_safe('<img src="/media/%s" width="100" height="100" style="object-fit: cover">' %(self.photo))
        else:
            return self.user.first_name[0]

    image_tag.short_description = 'ProfilePic'

class AllCourse (models.Model):
    courseTitle = models.CharField(max_length=100)
    courseDesc = RichTextField(null=True, blank=True)
    courseThumbnail = models.ImageField(upload_to="courseThumbnail/", null=True, blank=True, default="default.jpg")
    courseVideo = models.FileField(upload_to='sampleVideos/', null=True, blank=True)
    courseRating = models.DecimalField(max_digits=2, decimal_places=2,null=True, blank=True,)
    courseMajor = models.CharField(max_length=100, choices=[('Digital Media Technology', 'Digital Media Technology'), ('Game Development', 'Game Development'), ('Medical Media Innovation', 'Medical Media Innovation'), ('Media Technology', 'Media Technology')])
    courseYear = models.IntegerField(default=1, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    createBy = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    courseTaken = models.IntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        return self.courseTitle
    
    def Title (self):
        return self.courseTitle
    
    Title.short_description = 'Title'
    
    courseTitle.short_description = 'courseTitle'
    
    def image_tag(self):
        if self.courseThumbnail:
            return mark_safe('<img src="/media/%s" alt="" width="250">' %(self.courseThumbnail))
        else:
            return mark_safe('<img src="/media/default.png" alt="" width="100" height="100">')

    image_tag.short_description = 'Thumbnail'

class Lesson(models.Model):
    course = models.ForeignKey(AllCourse, on_delete=CASCADE)
    lessonTitle = models.CharField(max_length=100)

    def __str__(self):
        return '%s (%s)' % (self.course, self.lessonTitle)

class Video (models.Model) :
    lesson = models.ForeignKey(Lesson, on_delete=CASCADE, null=True, blank=True)
    videoTitle = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    
    def __str__(self):
        return '%s (%s)' % (self.lesson.lessonTitle, self.videoTitle)

class Homework (models.Model):
    course = models.ForeignKey(AllCourse, on_delete=CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=CASCADE, null=True, blank=True)
    homeworkTitle = models.CharField(max_length=100, null=True, blank=True)
    homework = models.FileField(upload_to='homeworks/', null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.lesson.lessonTitle, self.homeworkTitle)

class MyCourse (models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    courseId = models.IntegerField(null=True)
    course = models.ForeignKey(AllCourse, on_delete=CASCADE)
    stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '%s (%s)' % (self.user.user.first_name, self.course.courseTitle)
    
    def image_tag(self):
        if self.course.courseThumbnail:
            return mark_safe('<img src="/media/%s" alt="" width="250">' %(self.course.courseThumbnail))
        else:
            return mark_safe('<img src="/media/default.png" alt="" width="100" height="100">')

    image_tag.short_description = 'Thumbnail'
