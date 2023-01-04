from socket import fromshare
from django import forms
from datetime import datetime

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
        fields = Entryfields = ['topic','title','address','eligibility','image','text','selection_method']
        labels = {'topic': '','title': 'タイトル/事業者名','address':'事業所住所','eligibility':'応募資格','image':'画像を追加','text':'本文追加','selection_method':'選考方法'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80}), 'selection_method': forms.Textarea(attrs={'cols': 80})}

class ProfileForm(forms.ModelForm):
    """ユーザープロフィール設定フォーム"""
    class Meta:
        current_year = datetime.now().year
        min_year = current_year - 100
        model = Profile
        fields = ['family_name','first_name','sex','birthday','email','postal_code','prefectures','address','career','introduce']
        labels = {'family_name':'姓','first_name':'名前','sex':'性別','birthday':'生年月日','email':'emailアドレス','postal_code':'郵便番号', 'prefuctures':'都道府県', 'address':'都道府県以降の住所', 'career': '以前所属していた企業・役職', 'introduce':'自己PR'}
        widgets = {'introduce': forms.Textarea(attrs={'cols': 80}),'birthday':forms.SelectDateWidget(years=[x for x in range(min_year, current_year)])}

class SearchForm(forms.Form):
    keyword = forms.CharField(label='', max_length=50)