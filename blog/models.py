from django.db import models
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from taggit.managers import TaggableManager

# Create your models here.


class Blog (models.Model):
    title = models.CharField(max_length=300)
    composer = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    short_desc = models.TextField()
    blog_data = models.TextField()
    blog_image = models.ImageField(upload_to='blog/')
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def previous(self):
        ids = Blog.objects.all().values_list('id', flat=True)
        id_min = min(list(ids))
        if self.id > id_min:
            return (self.id - 1)

    def next(self):
        ids = Blog.objects.all().values_list('id', flat=True)
        id_max = max(list(ids))
        if self.id < id_max:
            return (self.id + 1)

    def jalali_date(self):
        return JalaliDate(self.date.date())

    def jalali_time(self):
        return JalaliDateTime(self.date).strftime("%H:%M")


class BlogComment(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    def __str__(self):
        return self.username

    def jalali_date(self):
        return JalaliDate(self.date.date())

    def jalali_time(self):
        return JalaliDateTime(self.date).strftime("%H:%M")
