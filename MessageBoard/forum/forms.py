from django.forms import ModelForm
from .models import Post, Reply
from django import forms
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(ModelForm):
    post_text = forms.CharField(widget=TinyMCEWidget(attrs={'required': False, 'cols': 30, 'rows': 30}), label='Текст объявления:')

    class Meta:
        model = Post
        fields = ['post_author', 'post_title', 'post_text', 'post_category']

        widgets = {
            'post_author': forms.HiddenInput(),
        }

        labels = {
            'post_title': 'Заголовок',
            'post_category': 'Категория',
        }


class ReplyForm(ModelForm):

    class Meta:
        model = Reply
        fields = ['reply_text', 'reply_author', 'reply_post']

        widgets = {
            'reply_author': forms.HiddenInput(),
            'reply_post': forms.HiddenInput(),
        }

        labels = {
            'reply_text': '',
        }

