from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, 'Your account was created. You are able to log in.')
			return redirect('accounts:login')
	else:
		form = UserRegisterForm()

	return render(request, 'accounts/register.html', dict(form=form))


class BestPlayersListView(ListView):
	model = Profile
	ordering = '-points'


def edit_profile(request):
	user = request.user
	if request.method == 'POST':
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
		user_form = UserUpdateForm(request.POST, instance=user)

		if profile_form.is_valid() and user_form.is_valid():
			profile_form.save()
			user_form.save()
			messages.success(request, 'Your account was updated.')
			return redirect('accounts:edit_profile')
	else:
		profile_form = ProfileUpdateForm(instance=user.profile)
		user_form = UserUpdateForm(instance=user)
	
	return render(request, 'accounts/profile.html', 
		dict(profile_form=profile_form, user_form=user_form))


class UserDetailView(DetailView, MultipleObjectMixin):
	model = User
	template_name = 'accounts/user_detail.html'
	paginate_by = 5

	def get_context_data(self, **kwargs):
		object_list = self.get_object().quizzes.all()
		context = super().get_context_data(object_list=object_list, **kwargs)
		return context
