from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.db.models import Q
from .models import Quiz, Question, Answer, Comment
from .forms import QuestionAndAnswersForm, CommentForm


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/home.html'
    ordering = '-date_created'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        if category:
            if category == 'All':
                return Quiz.objects.filter(
                    Q(author__username__icontains=query) |
                    Q(title__icontains=query) |
                    Q(description__icontains=query)
                ).order_by('-date_created').all()
            else:
                if query:
                    return Quiz.objects.filter((
                        Q(author__username__icontains=query) |
                        Q(title__icontains=query) |
                        Q(description__icontains=query)) &
                        Q(category__name__icontains=category)
                    ).order_by('-date_created').all()
                else:
                    return Quiz.objects.filter(category__name__icontains=category).order_by('-date_created')
        return super().get_queryset()


def quiz_detail(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    form = CommentForm()
    comments = quiz.comments.order_by('-date_commented').all()
    if request.method == 'POST':
        # Calculate the points
        data = request.POST.copy()
        points = 0
        choices_list = []
        for i, question in enumerate(quiz.questions.all()):
            if Answer.objects.get(pk=data.get(f'answer{question.id}')).is_correct:
                points += 1
            choices_list.append([question.question])
            choices = []
            for j in range(4):
                choices.append([
                    question.answers.all()[j], question.answers.all()[j].is_correct,
                    int(question.answers.all()[j].id) == int(data.get(f'answer{question.id}'))])
            choices_list[i].append(choices)

        # Add points to user profile
        if request.user.is_authenticated:
            request.user.profile.points += points
            request.user.profile.save()

        return render(request, 'quiz/quiz_detail.html', dict(quiz=quiz, form=form, comments=comments,
                                                             solved=choices_list, points=points))

    return render(request, 'quiz/quiz_detail.html', dict(quiz=quiz, form=form, comments=comments))


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ('title', 'description', 'category')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuizUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quiz
    fields = ('title', 'description', 'category')

    def test_func(self):
        return self.get_object().author == self.request.user


class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quiz
    success_url = '/'

    def test_func(self):
        return self.get_object().author == self.request.user


@login_required
def create_question(request, pk):
    if request.method == 'POST':
        form = QuestionAndAnswersForm(request.POST)

        if form.is_valid():
            question = Question.objects.create(question=form.cleaned_data['question'], quiz_id=pk)
            Answer.objects.create(answer=form.cleaned_data['correct_answer'],
                                  question=question, is_correct=True)
            Answer.objects.create(answer=form.cleaned_data['answer_2'],
                                  question=question, is_correct=False)
            Answer.objects.create(answer=form.cleaned_data['answer_3'],
                                  question=question, is_correct=False)
            Answer.objects.create(answer=form.cleaned_data['answer_4'],
                                  question=question, is_correct=False)
            messages.success(request, 'Question has been created.')
            return redirect('quiz:detail', pk=pk)
    else:
        form = QuestionAndAnswersForm()
    return render(request, 'quiz/question_form.html', dict(form=form))


@login_required
def update_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user != question.quiz.author:
        raise PermissionDenied()

    correct_answer = question.answers.filter(is_correct=True).first()
    answer_2 = question.answers.filter(is_correct=False).all()[0]
    answer_3 = question.answers.filter(is_correct=False).all()[1]
    answer_4 = question.answers.filter(is_correct=False).all()[2]
    initial = dict(question=question.question, correct_answer=correct_answer, answer_2=answer_2,
                   answer_3=answer_3, answer_4=answer_4)
    if request.method == 'POST':
        form = QuestionAndAnswersForm(request.POST, initial=initial)

        if form.is_valid():
            question.question = form.cleaned_data['question']
            correct_answer.answer = form.cleaned_data['correct_answer']
            answer_2.answer = form.cleaned_data['answer_2']
            answer_3.answer = form.cleaned_data['answer_3']
            answer_4.answer = form.cleaned_data['answer_4']
            question.save()
            correct_answer.save()
            answer_2.save()
            answer_3.save()
            answer_4.save()
            messages.success(request, 'Question has been updated.')
            return redirect('quiz:detail', pk=question.quiz.id)
    else:
        form = QuestionAndAnswersForm(initial=initial)
    return render(request, 'quiz/question_form.html', dict(form=form, update=True))


@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user != question.quiz.author:
        raise PermissionDenied()

    question.delete()
    return redirect('quiz:detail', pk=question.quiz.id)


@login_required
def comment(request, pk):
    if request.method == 'GET':
        return redirect('quiz:detail', pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.quiz_id = pk
        comment.user_id = request.user.id
        comment.save()
    return redirect('quiz:detail', pk=pk)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ('comment',)


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('quiz:detail', kwargs=dict(pk=self.get_object().quiz.id))


@login_required
def like(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.user in quiz.likes.all():
        quiz.likes.remove(request.user)
    else:
        if request.user in quiz.dislikes.all():
            quiz.dislikes.remove(request.user)
        quiz.likes.add(request.user)
    return JsonResponse({'likes': quiz.likes.count(), 'dislikes': quiz.dislikes.count()})


@login_required
def dislike(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.user in quiz.dislikes.all():
        quiz.dislikes.remove(request.user)
    else:
        if request.user in quiz.likes.all():
            quiz.likes.remove(request.user)
        quiz.dislikes.add(request.user)
    return JsonResponse({'likes': quiz.likes.count(), 'dislikes': quiz.dislikes.count()})

