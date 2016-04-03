from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

	
# Create your models here.
class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.
	date_creation = models.DateTimeField(default=datetime.now, blank=True, null=True)
	mobile_no = models.BigIntegerField(blank=True, null=True)

	class Meta:
		verbose_name = ('User Profile')
		verbose_name_plural = ('User Profiles')

	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username
