from socket import fromshare
from django import forms

from .models import Topic, Entry
# , UploadImage

class TopicForm(forms.ModelForm):
    """新規トピック追加用フォーム"""
    class Meta:
        model = Topic
        fields = {'text'}
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    """新規記事追加用フォーム"""
    topic = forms.ModelChoiceField(queryset=Topic.objects.all())
    class Meta:
        model = Entry
        fields = Entryfields = ['topic','title','eligibility','image','text']
        labels = {'topic': '','title': 'タイトル','eligibility':'応募資格','image':'画像を追加','text':'本文を追加'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

# class UploadForm(forms.ModelForm):
#     """新規記事画面の画像追加用フォーム"""
#     class Meta:
#         model = UploadImage
#         fields = ['image']