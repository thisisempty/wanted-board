from django.db import models
from django.db.models.deletion import CASCADE

from core.models import TimeStamp
from users.models import User

class Post(TimeStamp):
    uesr = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    
    class Meta:
        db_table = 'posts'