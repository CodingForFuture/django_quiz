from django.urls import path, include
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.QuizListView.as_view(), name='home'),
    path('create-quiz', views.QuizCreateView.as_view(), name='create_quiz'),
    path('quiz/<int:pk>', views.quiz_detail, name='detail'),
    path('quiz/<int:pk>/update', views.QuizUpdateView.as_view(), name='update'),
    path('quiz/<int:pk>/delete', views.QuizDeleteView.as_view(), name='delete'),
    path('quiz/<int:pk>/add-question', views.create_question, name='create_question'),
    path('quiz/question/<int:pk>/update', views.update_question, name='update_question'),
    path('quiz/question/<int:pk>/delete', views.delete_question, name='delete_question'),
    path('quiz/comment/<int:pk>', views.comment, name='comment'),
    path('quiz/comment/<int:pk>/update', views.CommentUpdateView.as_view(), name='update_comment'),
    path('quiz/comment/<int:pk>/delete', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('quiz/<int:pk>/like', views.like, name='like'),
    path('quiz/<int:pk>/dislike', views.dislike, name='dislike'),
]