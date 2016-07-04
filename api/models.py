from __future__ import unicode_literals
from django.db import models
import uuid

class User(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    login_email = models.EmailField(max_length=254,unique=True,blank=False,null=False)
    username = models.EmailField(max_length=254,unique=True,blank=False,null=False)
    password = models.CharField(max_length=254,blank=False,null=False,)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=False,null=True,blank=True)
    email_verified = models.BooleanField(default=False)
    number_of_main_groups = models.IntegerField(default=0)
    # services = models.ManyToManyField('Service', through='ServiceCredential')

    def __unicode__(self):
        return str(self.login_email)

    class Meta:
        unique_together = (
            "username",
            "login_email"
        )


class MainGroup(models.Model):
    name = models.CharField(max_length=254,blank=False,null=False,)
    user = models.ForeignKey('User',blank=False,null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.name)

class ResponsibilityType(models.Model):
    name = models.CharField(max_length=254,blank=False,null=False,)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.name)

class Service(models.Model):
    name = models.CharField(max_length=254,blank=False,null=False,)
    type = models.ForeignKey('ResponsibilityType',blank=False,null=False)
    logo_image_url = models.URLField(blank=False,null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    options = models.ManyToManyField('ServiceOption',blank=True,null=True)

    def __unicode__(self):
        return str(self.name)

class ServiceOption(models.Model):
    name = models.CharField(max_length=254,blank=False,null=False,)
    date_created = models.DateTimeField(auto_now_add=True)
    inputs = models.ManyToManyField('OptionInput',blank=True,null=True)
    map_required = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.name)

class OptionInput(models.Model):
    name = models.CharField(max_length=254,blank=False,null=False,)
    RADIO = 'radio'
    TEXT = 'text'
    EMAIL = 'email'
    NUMBER = 'number'
    CHECKBOX = 'checkbox'
    HIDDEN = 'hidden'
    INPUT_TYPES = (
        (RADIO, 'radio'),
        (TEXT, 'text'),
        (EMAIL, 'email'),
        (NUMBER, 'number'),
        (CHECKBOX, 'checkbox'),
        (HIDDEN, 'hidden'),
    )
    input_type = models.CharField(max_length=25,choices=INPUT_TYPES,default=TEXT)
    placeholder = models.CharField(max_length=254,blank=True,null=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    required = models.BooleanField(default=False)
    value_one = models.CharField(max_length=254, blank=True,null=True, default='')
    value_two = models.CharField(max_length=254, blank=True,null=True, default='')

    def __unicode__(self):
        return str(self.name)

# class ServiceCredential(models.Model):
#     service = models.ForeignKey('Service',blank=False,null=False)
#     user = models.ForeignKey('User',blank=False,null=False)
#     identifier = models.CharField(max_length=254,blank=True,null=True)
#     token = models.CharField(max_length=254,blank=True,null=True)
#
#     def __unicode__(self):
#         return str(self.id)

class Task(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    title = models.CharField(max_length=254,blank=False,null=False,)
    user = models.ForeignKey('User',blank=False,null=False)
    group = models.ForeignKey('MainGroup',blank=False,null=False)
    notes = models.CharField(max_length=254,blank=False,null=False,)
    service = models.ForeignKey('Service',blank=True,null=True)
    date = models.DateField(verbose_name="startDate",blank=False,null=False)
    time = models.TimeField(verbose_name="startTime",blank=False,null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.title)