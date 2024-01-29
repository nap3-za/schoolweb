from django.db import models
from django.conf import settings
from .utils import post_types
# Create your models here.

class Comment(models.Model):

	author  		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content 		= models.CharField(verbose_name="comment", max_length=250, null=False, blank=False)
	post 			= models.ForeignKey('Post', verbose_name="post", on_delete=models.CASCADE, blank=False, null=False)
	timestamp 		= models.DateTimeField(verbose_name="timestamp", auto_now_add=True)
	is_active 		= models.BooleanField(default=True, verbose_name="is_active")

	def __str__(self):
		return self.author.username

class Post(models.Model):

	author 		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="author")
	title 		= models.CharField(verbose_name="title", max_length=200, null=False, blank=False, unique=False)
	intro		= models.CharField(verbose_name="intro", max_length=500, blank=True, unique=False)
	content 	= models.CharField(verbose_name="content", max_length=5000, null=True, blank=True, unique=False)
	post_type 	= models.CharField(choices=post_types, verbose_name="post_type", null=False, blank=False, max_length=100, default='General')

	views 		= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="views", blank=True)
	comments 	= models.ManyToManyField(Comment, related_name="comments", blank=True)
	timestamp 	= models.DateTimeField(verbose_name="timestamp", auto_now_add=True)

	is_active 		= models.BooleanField(default=True, verbose_name="is_active")
	draft 		= models.BooleanField(verbose_name="draft", default=True)

	# Groups it will be visible to
	grade 		= models.BooleanField(verbose_name="grade", default=False)
	stream 		= models.BooleanField(verbose_name="stream", default=False)
	sport 		= models.BooleanField(verbose_name="sport", default=False)
	club 		= models.BooleanField(verbose_name="club", default=False)
	teachers 	= models.BooleanField(verbose_name="teachers", default=False)

	def __str__(self):
		return self.author.username + ' | ' + self.title
	
	def public(self):
		self.draft = False
		self.save()

	def is_draft(self):
		return self.is_draft

	def viewcount(self):
		viewcount = len(self.views)
		return viewcount

	def viewers(self):
		viewers = self.views.all()
		return viewers


