from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse


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
	likes = models.ManyToManyField(User, related_name='liked_quizzes')
	dislikes = models.ManyToManyField(User, related_name='disliked_quizzes')

	class Meta:
		verbose_name_plural = 'Quizzes'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('quiz:detail', kwargs=dict(pk=self.id))


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


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='comments')
	comment = models.CharField(max_length=300)
	date_commented = models.DateTimeField(default=now)

	def get_absolute_url(self):
		return reverse('quiz:detail', kwargs=dict(pk=self.quiz.pk))