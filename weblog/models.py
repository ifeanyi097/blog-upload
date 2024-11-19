from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
	full_name = models.CharField(max_length=200, blank=True, null=True)
	bio = models.CharField(max_length=500, blank=True, null=True)
	followers = models.ManyToManyField(User, related_name="user_followers")
	following = models.ManyToManyField(User, related_name="user_following")
	picture = models.FileField(upload_to="profile_pictures", blank=True, null=True)
	
	def count_followers(self):
		return self.followers.count()
		
	def count_following(self):
		return self.following.count()
		
	def __str__(self):
		return self.full_name
	

class Blog(models.Model):
	title = models.CharField(max_length=200)
	snippet = models.CharField(max_length=500)
	media = models.FileField(upload_to="blog_media")
	blogger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blogs")
	blog = models.TextField()
	likes = models.ManyToManyField(User, related_name="blog_likes")
	unlikes = models.ManyToManyField(User, related_name="blog_unlikes")
	date = models.DateTimeField(auto_now_add=True)
	is_public = models.BooleanField(default=False)
	
	
	def __str__(self):
		return self.title
		
		
class Comments(models.Model):
		blog = models.ForeignKey(Blog, related_name="blog_comments", on_delete=models.CASCADE)
		writer = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE)
		comment = models.CharField(max_length=500)
		date = models.DateTimeField(auto_now_add=True)