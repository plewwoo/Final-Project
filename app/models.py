from math import fabs
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.html import mark_safe
from django.db.models import Count
from ckeditor.fields import RichTextField
import random

from numpy import allclose

# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to="profilePic/", null=True, blank=True)
    tel = models.CharField(max_length=12, null=True, blank=True)
    major = models.CharField(max_length=100,null=True, blank=True, choices=[('dmt', 'Digital Media Technology'), ('gdm', 'Game Development'), ('mmi', 'Medical Media Innovation')])
    year = models.IntegerField(null=True, blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])
    userType = models.CharField(max_length=100, default="student", choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')])
    apply = models.BooleanField(default=False)
    
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
    courseRating = models.DecimalField(default=0, max_digits=19, decimal_places=1,null=True, blank=True,)
    courseMajor = models.CharField(max_length=100, choices=[('dmt', 'Digital Media Technology'), ('gdm', 'Game Development'), ('mmi', 'Medical Media Innovation'), ('mdt', 'Media Technology')])
    courseYear = models.IntegerField(default=1, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    createBy = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    courseTaken = models.IntegerField(default=0, null=True, blank=True)
    courseHours = models.CharField(max_length=100, null=True, blank=True, choices=[('น้อยกว่า 1 ชั่วโมง', 'น้อยกว่า 1 ชั่วโมง'), ('1 - 2 ชั่วโมง', '1 - 2 ชั่วโมง'), ('2 - 3 ชั่วโมง', '2 - 3 ชั่วโมง'), ('3 - 4 ชั่วโมง', '3 - 4 ชั่วโมง'), ('มากกว่า 4 ชั่วโมง', 'มากกว่า 4 ชั่วโมง')])
    
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

class Video (models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=CASCADE, null=True, blank=True)
    videoTitle = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    videoUrl = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return '%s (%s)' % (self.lesson.lessonTitle, self.videoTitle)
    
class VideoResult (models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    course = models.ForeignKey(AllCourse, on_delete=CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=CASCADE)
    video = models.ForeignKey(Video, on_delete=CASCADE)
    currentTime = models.IntegerField(default=0 ,null=True)
    watched = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s)' % (self.lesson.lessonTitle, self.video.videoTitle)

class MyCourse (models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    courseId = models.IntegerField(null=True)
    course = models.ForeignKey(AllCourse, on_delete=CASCADE)
    stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    numVideo = models.IntegerField(default=0, null=True, blank=True)
    progress = models.DecimalField(default=0, max_digits=19, decimal_places=2,null=True, blank=True)
    passedQuiz = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.user.user.first_name, self.course.courseTitle)
    
    def image_tag(self):
        if self.course.courseThumbnail:
            return mark_safe('<img src="/media/%s" alt="" width="250">' %(self.course.courseThumbnail))
        else:
            return mark_safe('<img src="/media/default.png" alt="" width="100" height="100">')

    image_tag.short_description = 'Thumbnail'

class TeacherPending (models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    interest = models.CharField(max_length=100)
    work = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)
    approve = models.BooleanField(default=False)
    applyDate = models.DateTimeField(auto_now_add=True)
    approveDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.user.user.first_name)
        
class Comment (models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    comment = RichTextField(null=True, blank=True)
    course = models.ForeignKey(AllCourse, on_delete=CASCADE)
    stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '%s %s (%s)' % (self.user.user.first_name, self.course, self.comment)

class Review (models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    rating = models.IntegerField(null=True, blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    review = models.CharField(max_length=500)
    course = models.ForeignKey(AllCourse, on_delete=CASCADE)

    def __str__(self):
        return '%s %s (%s)' % (self.user.user.first_name, self.course, self.review)

DIFF_CHOICES = (
    ('ง่าย', 'ง่าย'),
    ('ปานกลาง', 'ปานกลาง'),
    ('ยาก', 'ยาก'),
)

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    lesson = models.ForeignKey(Lesson, on_delete=CASCADE, null=True, blank=True)
    numberOfQuestions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    requiredScore = models.IntegerField(help_text="required score in %")
    difficulty = models.CharField(max_length=7, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.numberOfQuestions]

    class Meta:
        verbose_name_plural = 'Quizes'

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False, blank=True)
    question = models.ForeignKey(Question, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question.text}"

class Result(models.Model):
    course = models.ForeignKey(AllCourse, on_delete=CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=CASCADE)
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    score = models.FloatField()
    done = models.BooleanField(default=False)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.quiz)