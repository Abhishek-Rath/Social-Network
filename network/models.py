from django.contrib.auth.models import AbstractUser
from django.db import models
# from datetime import datetime
from django.utils import timezone

class User(AbstractUser):
    pass


class Post(models.Model):
    """
        Columns:
        user: User who posted the content (References user Class)
        post: Content posted (Charfield)
        data_and_time
        likes: No of likes post has
    """

    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "author")
    content = models.CharField(max_length = 255)
    date = models.DateTimeField(default = timezone.now)
    likes = models.IntegerField(default = 0)


    def __str__(self):
        return f"User: {self.user} has posted {self.content} on {self.date} having  {self.likes} likes"
