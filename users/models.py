from django.db import models

from core.models import TimeStamp

class User(TimeStamp):
    account_id = models.CharField(max_length=100)
    password   = models.CharField(max_length=200)

    class Meta:
        db_table = 'users'