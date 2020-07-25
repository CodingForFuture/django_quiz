from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Quiz, Category


class QuizListView(ListView):
	model = Quiz
	template_name = 'quiz/home.html'


class QuizCategoryListView(ListView):
	model = Quiz
	template_name = 'quiz/category.html'

	def get_queryset(self):
		category = get_object_or_404(Category, name=self.kwargs['category'])
		return category.quizzes.all()
