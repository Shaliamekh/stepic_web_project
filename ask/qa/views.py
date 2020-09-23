from django.shortcuts import render, reverse, get_object_or_404, Http404, HttpResponseRedirect, resolve_url
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import QuestionManager, Question, Answer
from .forms import AskForm, AnswerForm, SignUpForm, LogInForm
from django.contrib.auth import authenticate, login
import random


def test(request, *args, **kwargs):
    return HttpResponse('OK')

def paginate(request, questions):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(questions, 10)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page, paginator

def new(request):
    questions = Question.objects.new()
    page, paginator = paginate(request, questions)
    paginator.baseurl = reverse('new') + '?page='
    return render(request, 'qa/new.html', {'questions': page.object_list,
                                           'paginator': paginator,
                                           'page': page})


def popular(request):
    questions = Question.objects.popular()
    page, paginator = paginate(request, questions)
    paginator.baseurl = reverse('popular') + '?page='
    return render(request, 'qa/popular.html', {'questions': page.object_list,
                                               'paginator': paginator,
                                               'page': page})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answer_set.all()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.cleaned_data['author'] = request.user
            answer = form.save()
            return HttpResponseRedirect(reverse('q_detail', args=(question.id,)))
    else:
        form = AnswerForm(initial={'question': question})
    return render(request, 'qa/detail.html', {'question': question,
                                              'answers': answers, 'form': form})

def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form.cleaned_data['author'] = request.user
            question = form.save()
            return HttpResponseRedirect(reverse('q_detail', args=(question.id,)))
    else:
        form = AskForm()
        form._user = request.user
    return render(request, 'qa/ask.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('new'))
    else:
        form = SignUpForm()
    return render(request, 'qa/signup.html', {'form': form})

def login_form(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('new'))
    else:
        form = LogInForm()
    return render(request, 'qa/login.html', {'form': form})


