from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from PIL import Image

class userpost(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=100)
    message = models.TextField(max_length=700)
    author = models.CharField(max_length=100)
    # photo_thumb = models.ImageField(upload_to="user_post_photos")
    # photo_post = models.ImageField(upload_to="user_post_photos")
    photo = models.ImageField(upload_to="user_post_photos")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

    def save(self):
        super().save()

        size_for_thumb = (500, 550)
        pic_for_thumb = Image.open(self.photo.path)

        if pic_for_thumb.width < pic_for_thumb.height:
            # To reduce size of photo.
            pic_for_thumb.thumbnail(size_for_thumb)
            xcenter = pic_for_thumb.width / 2
            ycenter = pic_for_thumb.height / 2
            x1 = xcenter - 200
            y1 = 50
            x2 = xcenter + 200
            y2 = 500
            main_pic_for_thumb = pic_for_thumb.crop((x1, y1, x2, y2))
            # main_pic_for_thumb.show()
            main_pic_for_thumb.save(self.photo.path)

        elif pic_for_thumb.width > pic_for_thumb.height:
            size_for_thumb = (800, 850)
            pic_for_thumb.thumbnail(size_for_thumb)
            xcenter = pic_for_thumb.width / 2
            ycenter = pic_for_thumb.height / 2
            if pic_for_thumb.width < 500:
                x1 = 50
                y1 = ycenter - 400
                x2 = 850
                y2 = ycenter + 450
            else:
                x1 = xcenter - 200
                y1 = 0
                x2 = xcenter + 200
                y2 = 450
            main_pic_for_thumb = pic_for_thumb.crop((x1, y1, x2, y2))
            main_pic_for_thumb.save(self.photo.path)

        # img = Image.open(self.photo.path)
        # if img.height > 400 or img.width > 450:
        #     output_size = (400,450)
        #     img.thumbnail(output_size)
        #     img.save(self.photo.path)

class BlogComment(models.Model):
    sno = models.AutoField(primary_key = True)
    comment = models.CharField(max_length=400, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(userpost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.user + " commented '" + self.comment[:30] + "....' by " + self.user.username.upper()