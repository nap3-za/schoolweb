from django.db import models
from django.conf import settings
from .utils import sports, clubs, streams, grades

class LearnerAccount(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	# Extra fields
	stream 			= models.CharField(choices=streams, verbose_name="stream", max_length=100, null=True, blank=True)
	grade 			= models.IntegerField(choices=grades, verbose_name="grade", null=False, blank=False)
	sport 			= models.CharField(choices=sports, verbose_name="sport", max_length=100, null=True, blank=True)
	club 			= models.CharField(choices=clubs, verbose_name="club", max_length=100, null=True, blank=True)

	is_active 	= models.BooleanField(default=True)	

	def __str__(self):
		return self.user.username
	



