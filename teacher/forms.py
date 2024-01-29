from django import forms
from .models import TeacherAccount

class TeacherAccountRegistration(forms.ModelForm):


	class Meta:
		model = TeacherAccount
		fields = ('sport', 'stream1', 'stream2', 'sub1', 'sub2', 'sub3')
		
	sport 		= forms.CharField(max_length=100)
	
	stream1		= forms.CharField(max_length=200)
	stream2		= forms.CharField(max_length=200)

	sub1		= forms.CharField(max_length=200)	
	sub2 		= forms.CharField(max_length=200)
	sub3 		= forms.CharField(max_length=200)	

	def clean_all(self):
		sub1 = self.cleaned_data['sub1']
		sub2 = self.cleaned_data['sub2']
		sub3 = self.cleaned_data['sub3']

		if (sub1 == sub2) or (sub1 == sub3) or (sub2 == sub3):
			raise forms.ValidationError("You have a subject selected twice")

		stream1 = self.cleaned_data['stream1']
		stream2 = self.cleaned_data['stream2']
		if stream1 == stream2:
			raise forms.ValidationError("You have a stream selected twice")

class TeacherAccountEdit(forms.ModelForm):

	class Meta:
		model = TeacherAccount
		fields = ('sport', 'stream1', 'stream2', 'sub1', 'sub2', 'sub3')


	def clean_all(self):
		sub1 = self.cleaned_data['sub1']
		sub2 = self.cleaned_data['sub2']
		sub3 = self.cleaned_data['sub3']

		if (sub1 == sub2) or (sub1 == sub3) or (sub2 == sub3):
			raise forms.ValidationError("You have a subject selected twice")

		stream1 = self.cleaned_data['stream1']
		stream2 = self.cleaned_data['stream2']
		if stream1 == stream2:
			raise forms.ValidationError("You have a stream selected twice")
