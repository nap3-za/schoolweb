from django import forms
from .models import LearnerAccount

class LearnerAccountRegistration(forms.ModelForm):

    class Meta:
        model = LearnerAccount
        fields = ('grade', 'stream', 'sport', 'club')

    grade           = forms.IntegerField(required=True, min_value=7, max_value=12)
    stream          = forms.CharField(required=True, max_length=100)
    sport           = forms.CharField(required=True, max_length=100)
    club            = forms.CharField(required=True, max_length=100)


    def clean(self):
        grade = self.cleaned_data['grade']
        stream = self.cleaned_data['stream']
        if stream != 'None' and grade < 10:
            raise  forms.ValidationError("You cannot pick a stream because of your grade")
        elif grade >= 10 and stream == 'None':
            raise forms.ValidationError(f"You must pick a valid stream if you are in grade {grade}")



class LearnerAccountEdit(forms.ModelForm):

    class Meta:
        model = LearnerAccount
        fields = ('grade', 'stream', 'sport', 'club')

    def clean(self):
        grade = self.cleaned_data['grade']
        stream = self.cleaned_data['stream']
        if stream != 'None' and grade < 10:
            raise  forms.ValidationError("You cannot pick a stream because of your grade")
        elif grade >= 10 and stream == 'None':
            raise forms.ValidationError(f"You must pick a valid stream if you are in grade {grade}")
 



