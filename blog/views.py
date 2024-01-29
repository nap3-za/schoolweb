from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from account.models import BaseAccount
from .form import CreatePostForm, UpdatePostForm, EditCommentForm
import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

# Optimized

def blog_home_view(request, *args, **kwargs):
	auth_user = request.user
	
	if not auth_user.is_authenticated:
		return redirect('login')

	if auth_user.is_authenticated:
		return render(request, "blog/blog.html")


# Optimized

def create_post_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return render(request,template_name="errors/not_auth.html")

	if auth_user.is_authenticated:
		try:
			auth_account = BaseAccount.objects.get(id=auth_user.id)
		except:
			return render(request, template_name="errors/does_not_exist.html")

		context['account'] = auth_account

		# If the form is being submitted
		if request.method == "POST":
			try:
				if request.POST:
					form = CreatePostForm(request.POST)
					if form.is_valid:
						print("[+] Form is valid and is saved")
						try:
							post = form.save(author=auth_account)
							return redirect('post' , post_id=post.id)
						except:
							print("[-] Form won't save")
					else:
						form = CreatePostForm(request.POST)
						context['form'] = form
			
			except Exception as e:
				return render(request, template_name="errors/try_again.html")
				print(str(e))

	return render(request, template_name="blog/post/create.html")

# post id
# Optimized

def update_post_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	if auth_user.is_authenticated:
		post_id = kwargs.get("post_id")
		
		try:
			auth_account = BaseAccount.objects.get(id=auth_user.id)
			post = Post.objects.get(id=post_id)
			context['post'] = post

		except BaseAccount.DoesNotExist or Post.DoesNotExist:
			return render(request, "errors.does_not_exist.html")

		if auth_account and request.method == "POST":
			form = UpdatePostForm(request.POST, instance=post)
			if form.is_valid:
				try:
					form.save()
					print("[+] Form is saved")
					return redirect('post', post_id=post_id)
				except Exception as e:
					form = UpdatePostForm(request.POST, instance=post)
					context['form'] = form	
					print("[-] Errors : "+str(e))
			else:
				form = UpdatePostForm(request.POST, instance=post)
				context['form'] = form	

	return render(request, "blog/post/update.html", context)


# Optimized
@login_required(login_url="login")
def delete_post_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	elif auth_user.is_authenticated:
		auth_user_account = BaseAccount.objects.get(id=auth_user.id)
		try:
			post_id = kwargs.get('post_id')
			if post_id:
				post = Post.objects.get(id=post_id)
				if auth_user_account and post:
					if post.author == auth_user_account:
						post.is_active = False
						post.save()
						return redirect('my_posts')
					else:
						return render(request, template_name="errors/not_allowed.html")
				else:
					return render(request, template_name="errors/does_not_exist.html")
		except:
			return render(request, "errors/try_again.html")

	return render(request, "blog/post/delete.html", context)

# Optimized
@login_required(login_url="login")
def post_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return render(request, template_name="errors/not_auth.html")

	if auth_user.is_authenticated:
		post_id = kwargs.get("post_id")
		
		if post_id:
			post = Post.objects.get(id=post_id)
			if post:
				context['post'] = post
				comments = []
				# get the authenticated users friend list
				comment_model = Comment.objects.filter(post=post, is_active=True).order_by('-timestamp')
				if comment_model:
					for comment in comment_model:
						is_mine = None
						if comment.author == auth_user:
							my_comment = True
						else:
							my_comment = False

						if comment.post == post and comment.is_active == True:
							comments.append((comment, my_comment))

				context['comments'] = comments
				# Viewcount feature
				if post.author != auth_user:
					post.views.add(auth_user)
					post.save()

				viewers = post.views.all()
				context['views'] = viewers

				if auth_user == post.author:
					is_mine = True
					context['is_mine'] = is_mine
				else:
					is_mine = False
					context['is_mine'] = is_mine
			else:
				return render(request, template_name="errors/does_not_exist.html")
		else:
			return render(request, template_name="errors/not_allowed.html")

	return render(request, "blog/post/post.html", context)

# Optimized
@login_required(login_url="login")
def posts_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	elif auth_user.is_authenticated:
		auth_user_account = BaseAccount.objects.get(id=auth_user.id)
		try:
			posts = []
			posts_list = Post.objects.filter(is_active=True).order_by('-timestamp')
			if posts_list:
				for post in posts_list:
					is_mine = False
					if auth_user_account == post.author:
						is_mine = True
					if not post.draft:
						posts.append((post, is_mine))
				# Pagination
				p = Paginator(posts, 5)
				page = request.GET.get('page')
				posts_list_paginated = p.get_page(page)
				context['posts'] = posts_list_paginated
			else:
				return render(request, template_name="errors/try_again.html")	
		except:
			return render(request, template_name="errors/does_not_exist.html")

	return render(request, "blog/post/posts.html", context)

# Optimized
@login_required(login_url="login")
def my_posts_view(request, *args, **kwargs):

	print('[+] My posts view runnign')
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	elif auth_user.is_authenticated:

		auth_user_account = BaseAccount.objects.get(id=auth_user.id)

		try:
			posts_list = Post.objects.filter(is_active=True, author=auth_user_account).order_by('-timestamp')
			# Pagination
			p = Paginator(posts_list, 5)
			page = request.GET.get('page')
			posts_list_paginated = p.get_page(page)
			context['posts'] = posts_list_paginated
		except:
			return render(request, template_name="errors/does_not_exist.html")

	return render(request, "blog/post/my_posts.html", context)

# Optimized
@login_required(login_url="login")
def search_posts_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	elif auth_user.is_authenticated:

		if request.method == "GET":
			search_query = request.GET.get("q")
			if len(search_query) > 0:
				search_results = Post.objects.filter(title__icontains=search_query).distinct().order_by('-timestamp')

				# [(post1, True), (post2, False), ...]
				posts = []
				for post in search_results:
					if user == post.author:
						is_mine = True
					else:
						is_mine = False
					posts.append((post, is_mine))
				context['posts'] = posts
				
	return render(request, "blog/search.html", context)

# Optimized
@login_required(login_url="login")
def add_comment_view(request, *args, **kwargs):
	context = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return redirect('login')

	elif auth_user.is_authenticated:
		auth_user_account = BaseAccount.objects.get(id=auth_user.id)

		if request.method == "POST":
			post_id = kwargs.get("post_id")

			payload = {
				"response" : ""
			}
			
			if post_id:
				comment = request.POST.get("data")
				author = auth_user_account
				post = Post.objects.get(id=post_id)
				if comment and post:
					comment = Comment.objects.create(author=author, content=comment, post=post)
					comment.save()
					payload['response'] = "[+] Comment added"
				else:
					payload['response'] = "[-] Models do not exists"
					return render(request, "errors/does_not_exist.html")
			else:
				payload['response'] = "Keyword args are not valid"
				return render(request, "errors/does_not_exist.html")

		if payload['response'] == None:
			payload['response'] = "Default because it was none"
	else:
		return redirect('login')

	return HttpResponse(json.dumps(payload), content_type="application/json")

# Optimized
@login_required(login_url="login")
def edit_comment_view(request, *args, **kwargs):
	payload = {}
	auth_user = request.user

	if not auth_user.is_authenticated:
		return render(request, template_name="errors/not_auth.html")

	elif auth_user.is_authenticated:
		try:
			comment_id = kwargs.get("comment_id")
			post_id = kwargs.get('post_id')

			if post_id and comment_id:
				try:
					post = Post.objects.get(id=post_id)
					comment = Comment.objects.get(id=comment_id)
					if post and comment:
						if not comment.author == auth_user:
							return render(request, template_name="erros/not_allowed.html")

						if request.method == "POST":
							form = EditCommentForm(request.POST)
							if form.is_valid():
								content = request.POST.get("content")
								comment.content = content
								comment.save()
								return redirect('post', post_id=post_id)
								print("[+] Edit comment form is saved")
							else:
								form = EditCommentForm(request.POST)
								context['form'] = form
					else:
						return render(request, template_name="errors/does_not_allowed.html")
				
				except Exception as e:
					print("[+] Error : "+str(e))
		
		except Exception as e:
			print("[+] Error : "+str(e))

	return redirect('post', post_id=post_id, user_id=user.id)

# Optimized
@login_required(login_url="login")
def delete_comment_view(request, *args, **kwargs):
	auth_user = request.user
	context = {}

	if not auth_user.is_authenticated:
		return render(request, template_name="errors.not_auth.html")

	if auth_user.is_authenticated:
		comment_id = kwargs.get("comment_id")
		post_id = kwargs.get("post_id")

		if comment_id and post_id:
			try:
				comment = Comment.objects.get(id=comment_id)
				post = Post.objects.get(id=post_id)

				if comment.author == auth_user:
					comment.is_active = False
					comment.save()
					return redirect('post', post_id=post_id)
				else:
					return render(request, template_name="errors/not_allowed.html")
			except Exception as e:
				print("[-] Error : "+str(e))
				return render(request, template_name="errors/does_not_exist.html")
		else:
			return render(request, template_name="errors/does_not_exist.html")