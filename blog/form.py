from django import forms
from .models import Post, Comment


class CreatePostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'intro', 'content', 'draft', 'teachers', 'grade', 'sport', 'club', 'stream', 'draft')

	def clean(self):
		title = self.cleaned_data['title']
		draft = self.cleaned_data['draft']
		intro = self.cleaned_data['intro']
		content = self.cleaned_data['content']
		teachers = self.cleaned_data['teachers']
		grade = self.cleaned_data['grade']
		sport = self.cleaned_data['sport']
		club = self.cleaned_data['club']
		stream = self.cleaned_data['stream']
		if not (title, intro, content, draft, teachers, grade, sport, club, stream, draft):
			raise forms.ValidationError("Please fill all the fields")

	def save(self, author, commit=True):
		post = super(CreatePostForm, self).save(commit=False)
		title = self.cleaned_data['title']
		intro = self.cleaned_data['intro']
		content = self.cleaned_data['content']
		draft = self.cleaned_data['draft']
		teachers = self.cleaned_data['teachers']
		grade = self.cleaned_data['grade']
		sport = self.cleaned_data['sport']
		club = self.cleaned_data['club']
		stream = self.cleaned_data['stream']
		post = Post.objects.create(author=author,title=title, intro=intro, content=content, draft=draft, teachers=teachers, grade=grade, sport=sport, club=club, stream=stream)
		if commit:
			post.save()
			print()
		return post


class UpdatePostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'intro', 'content', 'draft', 'teachers', 'grade', 'sport', 'club', 'stream')

	def save(self, commit=True):
		post = super(UpdatePostForm, self).save(commit=False)
		post.title = self.cleaned_data['title']
		post.intro = self.cleaned_data['intro']
		post.content = self.cleaned_data['content']

		post.draft = self.cleaned_data['draft']
		post.teachers = self.cleaned_data['teachers']
		post.club = self.cleaned_data['club']
		post.grade = self.cleaned_data['grade']
		post.sport = self.cleaned_data['sport']
		post.stream = self.cleaned_data['stream']
		if commit:
			post.save()
		return post


class EditCommentForm(forms.Form):

	content 		= forms.CharField(max_length=5000, required=True)
	comment_id 		= forms.IntegerField()

	def clean_content(self):
		content = self.cleaned_data['content']
		return content

	def clean_comment_id(self):
		comment_id = self.cleaned_data['comment_id']
		if comment_id != None:
			return comment_id



	
