from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Category(models.Model):
	name = models.CharField(max_length=64)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name


class Quiz(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='quizzes')
	date_created = models.DateTimeField(default=now)

	class Meta:
		verbose_name_plural = 'Quizzes'

	def __str__(self):
		return self.title


class Question(models.Model):
	question = models.CharField(max_length=100)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

	def __str__(self):
		return self.question


class Answer(models.Model):
	answer = models.CharField(max_length=100)
	is_correct = models.BooleanField()
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

	def __str__(self):
		return self.answer