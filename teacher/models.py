from django.db import models
from django.conf import settings
from .utils import subjects, streams, sports

# Create your models here.

class TeacherAccount(models.Model):
	user		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	# Extra fields
	sport 		= models.CharField(choices=sports, verbose_name="sport", max_length=100, null=True, blank=True)
	stream1		= models.CharField(choices=streams, verbose_name="stream1", max_length=200, null=True, blank=True)
	stream2		= models.CharField(choices=streams, verbose_name="stream2", max_length=200, null=True, blank=True)

	sub1		= models.CharField(choices=subjects, verbose_name="sub1", blank=False, null=False, max_length=200)	
	sub2 		= models.CharField(choices=subjects, verbose_name="sub2", blank=True, null=False, max_length=200)
	sub3 		= models.CharField(choices=subjects, verbose_name="sub3", blank=True, null=True, max_length=200)

	is_active 	= models.BooleanField(default=True)	
	
	def __str__(self):
		return self.user.name

	def get_subjects(self):
		subject = [str(self.sub1), str(self.sub2), str(self.sub3)]
		subjects = []
		try:
			for sub in subject:
				if sub == 'None':
					pass
				elif sub != 'None':
					subjects.append(str(sub))
				else:
					print('')
		except:
			return None

		return subjects

	def get_streams(self):
		stream = [str(self.stream1), str(self.stream2), str(self.stream3)]
		streams = []
		try:
			for stream in stream:
				if stream == 'None':
					pass
				elif stream != 'None':
					streams.append(str(stream))
		except:
			return None

		return streams


		