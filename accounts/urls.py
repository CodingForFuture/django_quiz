from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    # User authentication system
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User profiles system
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user_view'),
    path('best-players/', views.BestPlayersListView.as_view(), name='best_players'),
]
