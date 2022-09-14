from socket import fromshare
from django import forms

from .models import Topic, Entry, UploadImage
# , UploadImage

class TopicForm(forms.ModelForm):
    """新規トピック追加用フォーム"""
    class Meta:
        model = Topic
        fields = {'text'}
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    """新規記事追加用フォーム"""
    class Meta:
        model = Entry
        fields = Entryfields = ['text','image']
        labels = {'text': '','image':''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class UploadForm(forms.ModelForm):
    """新規記事画面の画像追加用フォーム"""
    class Meta:
        model = UploadImage
        fields = ['image']