from __future__ import unicode_literals
from django.db import models


class Profile(models.Model):
    profileID=models.CharField(max_length=16, unique=True)
    # Need more in here!

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
