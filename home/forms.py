from django import forms
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "postpic"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_content"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

class MessagesForm(forms.ModelForm):
    class Meta:
        model = Chat_Messages
        fields = '__all__'

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']

class ContactForm(forms.Form):
    username = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

