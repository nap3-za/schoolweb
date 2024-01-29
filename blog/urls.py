from django.urls import path
from .views import (
	blog_home_view,
	create_post_view,
	update_post_view,
	delete_post_view,
	post_view,
	posts_view,
	my_posts_view,
	search_posts_view,
	add_comment_view,
	edit_comment_view,
	delete_comment_view,
)

urlpatterns = [
	path('blog_home/', blog_home_view, name="blog_home"),
	path('blog/create_post/', create_post_view, name="create_post"),
	path('blog/<int:post_id>/update/', update_post_view, name="update_post"),
	path('blog/<int:post_id>/delete/', delete_post_view, name="delete_post"),
	path('blog/<int:post_id>/', post_view, name="post"),

	path('blog/posts/', posts_view, name="all_posts"),

	path('blog/my-posts/', my_posts_view, name="my_posts"),

	path('blog/posts/search/', search_posts_view, name="search_posts"),
	path('blog/<int:post_id>/comment/', add_comment_view, name="add_comment"),
	path('post/<int:post_id>/<comment_id>/edit/', edit_comment_view, name="edit_comment"),
	path('post/<int:post_id>/<comment_id>/delete/', delete_comment_view, name="delete_comment")
]
