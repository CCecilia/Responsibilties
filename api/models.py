from __future__ import unicode_literals
from django.db import models
import uuid

class User(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    login_email = models.EmailField(max_length=254,unique=True,blank=False,null=False)
    username = models.EmailField(max_length=254,unique=True,blank=False,null=False)
    password = models.CharField(max_length=254,blank=False,null=False,)

    def __unicode__(self):
        return str(self.email)

    class Meta:
        unique_together = ("username", "login_email")