#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class MsgBoard(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.username
    class Meta:
        ordering = ['-datetime']
