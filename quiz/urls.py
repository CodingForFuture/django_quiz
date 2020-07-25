from django.urls import path, include
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.QuizListView.as_view(), name='home'),
    path('category/<category>', views.QuizCategoryListView.as_view(), name='category')
]