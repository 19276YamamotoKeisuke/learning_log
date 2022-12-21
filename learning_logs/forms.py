from socket import fromshare
from django import forms

from .models import Topic, Entry, Profile
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

class ProfileForm(forms.ModelForm):
    """ユーザープロフィール設定フォーム"""
    class Meta:
        model = Profile
        fields = ['postal_code','prefectures','address','career','introduce']
        labels = {'postal_code':'郵便番号', 'prefuctures':'都道府県', 'address':'都道府県以降の住所', 'career': '以前所属していた企業・役職', 'introduce':'自己PR'}
        widgets = {'introduce': forms.Textarea(attrs={'cols': 80})}

# class ApplyForm(forms.ModelForm):
#     """応募フォームhidden"""
#     class Meta:
#         model = Apply
#         fields = {'entry_id','owner_id','applicant_id'}
#         labels = {'entry_id':'', 'owner_id':'', 'applicant_id':'' }