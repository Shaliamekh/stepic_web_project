from django.shortcuts import render, reverse, get_object_or_404, Http404
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from .models import QuestionManager, Question, Answer
from .forms import AskForm, AnswerForm


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
            answer = form.save()
            return HttpResponseRedirect(reverse('q_detail', args=(question.id,)))
    else:
        form = AnswerForm(initial={'question': question})
    return render(request, 'qa/detail.html', {'question': question, 'answers': answers, 'form': form})

def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(reverse('q_detail', args=(question.id,)))
    else:
        form = AskForm()
