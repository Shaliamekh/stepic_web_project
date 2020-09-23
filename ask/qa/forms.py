from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User

class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question

    def clean(self):
        pass

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput)

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer

    def clean(self):
        pass

class SignUpForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        return user

class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user
