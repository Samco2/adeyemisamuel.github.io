from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profl_pic = models.ImageField(null=True, blank=True, upload_to="img", default="/img/user.png")
    twitter = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profl_pic.path)

        if img.height > 300 or img.width > 300:
           output_size = (300, 300)
           img.thumbnail(output_size)
           img.save(self.profl_pic.path)
