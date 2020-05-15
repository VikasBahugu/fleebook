from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class SigningUser(models.Model):
    sno = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=213, null=True, blank=True, default="")
    lname = models.CharField(max_length=213, null=True, blank=True, default="")
    username = models.CharField(max_length=213, null=True, blank=True, default="")
    number_email = models.CharField(max_length=213, null=True, blank=True, default="")
    gender = models.CharField(max_length=10, null=True, blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.fname+ " " + self.lname + ' as ' + self.username

class ContactUser(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=213)
    email = models.CharField(max_length=213)
    subject = models.CharField(max_length=213)
    matter = models.CharField(max_length=513)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.email

class Profile(models.Model):
    sno = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=213, null=True, blank=True, default="")
    username = models.CharField(max_length=60, null=True, blank=True, default="")
    photo = models.ImageField(upload_to="profile", default='profile/default.png')

    dob = models.CharField(max_length=213, null=True, blank=True, default="")
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    marrystatus = models.CharField(max_length=30, blank=True, default="", null=True)
    address = models.CharField(max_length=213,  null=True, default="", blank=True)
    occupation = models.CharField(max_length=300, default="", blank=True, null=True)
    number = models.CharField(max_length=213, default="", blank=True, null=True)
    email = models.CharField(max_length=213, blank=True, default="", null=True)
    languages = models.CharField(max_length=213, blank=True, default="", null=True)
    bio = models.TextField(max_length=513, blank=True, default="", null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return self.fullname + ' as ' + self.username

    def save(self):
        super().save()
        size_for_thumb = (500, 550)
        pic_for_thumb = Image.open(self.photo.path)
        pic_for_thumb.thumbnail(size_for_thumb)
        pic_for_thumb.save(self.photo.path)
