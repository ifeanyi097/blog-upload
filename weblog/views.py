from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, get_user_model, login
from django.db.models import Count

from .models import *

# Create your views here.
def index(request):
	blogs = Blog.objects.filter(is_public=True).order_by("-date")
	return render(request, "weblog/index.html", {"blogs":blogs})

def signup(request):
	context = {"errors":[],}
	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")
		password = request.POST.get("password")
		password2 = request.POST.get("password2")
		us = username.strip()
		if len(us) < 5:
			context["errors"].append("username must not be less than five characters")
			context["username"] = username
			context["email"] = email
			
		
		if len(password.strip()) < 4:
			context["errors"].append("password less than 4 charracters")
		if password != password2:
			context["errors"].append("password does not match")
			
		if len(context)  > 1 or len(context["errors"]) > 0:
			
			return render(request, "weblog/signup.html", context)
		else:
			user = get_user_model().objects.create_user(username=username, email=email,password=password)
			login(request, user)
			UserProfile.objects.create(user=user)
			return redirect("profile", user.id)
	return render(request, "weblog/signup.html", context)
	

def profile(request, id):
	try:
		user = User.objects.get(id=id)
		blogs = user.user_blogs.filter(is_public=True).order_by("-date").annotate(total_comments=Count("blog_comments"))
		followings = user.user_followers.count()
		profile = user.user_profile
		blog_count = blogs.count()
		total_likes = blogs.aggregate(total_likes=Count('likes'))["total_likes"]
		total_unlikes = blogs.aggregate(total_unlikes=Count('unlikes'))["total_unlikes"]
		
		return render(request, "weblog/profile.html",{"profile":profile, "blogs":blogs, "blog_count":blog_count, "total_likes":total_likes, "total_unlikes":total_unlikes, "followings":followings})
	except UserProfile.DoesNotExist:
		raise Http404("not found")
		

def edit_profile(request, id):
	try:
		profile = UserProfile.objects.get(id=id)
		if request.method == "POST":
			full_name = request.POST.get("full_name").strip()
			bio = request.POST.get("bio").strip()
			if full_name:
				profile.full_name = full_name.title()
			if bio:
				profile.bio = bio
			if request.FILES:
				profile.picture = request.FILES.get("picture")
			
			profile.save()
			return redirect("profile", profile.user.id)
			
		return render(request, 'weblog/edit_profile.html', {"profile":profile})
	except UserProfile.DoesNotExist:
		return Http404("error page")
		
		
def new_blog(request, id):
	try:
		user = get_user_model().objects.get(id=id)
		context = {"profile":user.user_profile}
		if request.method == "POST":
			
			title = request.POST.get("title").strip()
			snippet = request.POST.get("snippet").strip()
			is_public = request.POST.get("is_public")
			blog = request.POST.get("blog").strip()
			
			if len(title) < 5:
				context["title"] = title
				context["blog"] = blog
				context["snippet"] = snippet
				context["t_errors"] = "title is too short"
			if len(blog) < 20:
				context["blog"] = blog
				context["title"] = title
				context["snippet"] = snippet
				context["b_errors"] = "blog must be at least 20 characters"
			
			if len(context) > 1:
				return render(request, "weblog/new_blog.html", context)
			
			new_blog = Blog(blogger=user, title=title, blog=blog)
			
			if len(snippet) > 0:
				new_blog.snippet = snippet
				
		
			
			if request.FILES:
				new_blog.media = request.FILES.get("media")
				
			if is_public == "public":
				new_blog.is_public = True
			
			new_blog.save()
				
			return redirect("profile", user.id)
			
			
				
		return render(request, "weblog/new_blog.html", context)
	except Blog.DoesNotExist:
		return Http404("page error")
		
		
def blog(request, id):
	try:
		blog = Blog.objects.get(id=id)
		comments = blog.blog_comments.all().order_by("-date")
		return render(request, "weblog/blog.html", {"blog":blog, "comments":comments})
	
	except Blog.DoesNotExist:
		return Http404("not found")
		

def signin(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("home")
		else:
			return render(request, "weblog/signin.html", {"error":"incorrect username or password. Try again"})
	return render(request, "weblog/signin.html", {"error":""})

def create_profile(request, id):
	try:
		user = User.objects.get(id=id)
		UserProfile.objects.create(user=user)
		return redirect("profile", user.id)
	except User.DoesNotExist:
		return Http404("not found")
		
def like(request, action, other, id):
	if action == "likes":
		try:
			blog = Blog.objects.get(id=id)
			user = request.user
			if user.is_authenticated:
				if blog.blogger == user:
					return JsonResponse({"error":"you can't  react to your own blog"})
				
				if user not in blog.likes.all() and user not in blog.unlikes.all():
					blog.likes.add(user)
					likes = blog.likes.count()
					unlikes = blog.unlikes.count()
					return JsonResponse({"status":"ok", "likes":likes,"unlikes":unlikes})
				
				elif user in blog.unlikes.all() and user not in blog.likes.all():
				
					blog.unlikes.remove(user)
					blog.likes.add(user)
					likes = blog.likes.count()
					unlikes = blog.unlikes.count()
					return JsonResponse({"status":"ok", "likes":likes,"unlikes":unlikes})
				
				else:
					blog.likes.remove(user)
					likes = blog.likes.count()
					unlikes = blog.unlikes.count()
					return JsonResponse({"status":"ok","likes":likes,"unlikes":unlikes})
			else:
				return JsonResponse({"error":"you must be logged in"})
		except Blog.DoesNotExist:
			return Http404("blog not found")
	else:
			
		try:
			blog = Blog.objects.get(id=id)
			user = request.user
			if user.is_authenticated:
				if blog.blogger == user:
					return JsonResponse({"error":"you can't  react to your own blog"})
				
				if user not in blog.unlikes.all() and user not in blog.likes.all():
					blog.unlikes.add(user)
					likes = blog.likes.count()
					unlikes = blog.unlikes.count()
					return JsonResponse({"status":"ok", "likes":likes,"unlikes":unlikes})
				
				elif user in blog.likes.all() and user not in blog.unlikes.all():
				
					blog.likes.remove(user)
					blog.unlikes.add(user)
					likes = blog.likes.count()
					unlikes = blog.unlikes.count()
					return JsonResponse({"status":"ok", "likes":likes,"unlikes":unlikes})
				
				else:
					blog.unlikes.remove(user)
					likes = blog.likes.count()
					unlikes = blog.unlikes.count()
					return JsonResponse({"status":"ok","likes":likes,"unlikes":unlikes})
			else:
				return JsonResponse({"error":"you must be logged in"})
		except Blog.DoesNotExist:
			return Http404("blog not found")
			
def follow(request, id):
			try:
				pro = UserProfile.objects.get(id=id)
				user = request.user
				if not user.is_authenticated:
					return JsonResponse({"error":"you are not logged in"})
				
				if user == pro.user:
					return JsonResponse({"error":"you cannot follow yourself"})
				
				if user in pro.followers.all():
						pro.followers.remove(user)
						followers = pro.followers.count()
						return JsonResponse({"status":"ok", "followers":followers})
				
				if not user in pro.followers.all():
					pro.followers.add(user)
					followers = pro.followers.count()
					return JsonResponse({"status":"ok", "followers":followers})
			except UserProfile.DoesNotExist:
					return Http404("unable to respond")
					

def new_comment(request, id):
	try:
		blog = Blog.objects.get(id=id)
		user = request.user
		comment = request.POST.get("comment").strip()
		if not user.is_authenticated:
			return JsonResponse({"error":"you are not logged in"})
		
		if comment:
			new_comment = Comments.objects.create(writer=user, blog=blog, comment=comment)
			if user.user_profile.full_name:
				writer = new_comment.writer.user_profile.full_name
				id = new_comment.writer.id
				newComment = new_comment.comment
				return JsonResponse({"status":"ok", "new_comment":newComment, "writer":writer, "id":id})
			else:
				return JsonResponse({"status":"incomplete"})
	except Blog.DoesNotExist:
		return Http404("unable to respond")
					
			