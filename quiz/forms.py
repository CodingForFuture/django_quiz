from django import forms
from .models import Comment


class QuestionAndAnswersForm(forms.Form):
	question = forms.CharField(max_length=100)
	correct_answer = forms.CharField(max_length=100)
	answer_2 = forms.CharField(max_length=100)
	answer_3 = forms.CharField(max_length=100)
	answer_4 = forms.CharField(max_length=100)


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment', )