from socket import fromshare
from django import forms
from datetime import datetime

from .models import Topic, Entry, Profile, Apply, Recommend
# , UploadImage

class ApplyForm(forms.ModelForm):
    """応募時履歴書&自己PR追加フォーム"""
    class Meta:
        model = Apply
        fields = ['PRtext','resume']
        labels = {'PRtext':'自己PR文','resume':'履歴書をアップロードする'}
        widgets = {'PRtext': forms.Textarea(attrs={'class': 'form-control'})}

class RecommendForm(forms.ModelForm):
    """会社からの記事のおススメ"""
    # entry = forms.ModelChoiceField(queryset=Entry.objects.filter(owner=))
    class Meta:
        model = Recommend
        fields = ['entry','text']
        labels = {'entry':'おすすめする記事を選択','text':'PR文'}
        widgets = {
            'text': forms.Textarea({'class':'form-control'}),
        }

class TopicForm(forms.ModelForm):
    """新規トピック追加用フォーム"""
    class Meta:
        model = Topic
        fields = {'text'}
        labels = {'text': ''}
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EntryForm(forms.ModelForm):
    """新規記事追加用フォーム"""
    topic = forms.ModelChoiceField(queryset=Topic.objects.all())
    class Meta:
        model = Entry
        fields = Entryfields = ['topic','title','address','eligibility','image','text','selection_method']
        labels = {'topic': '','title': 'タイトル','address':'事業所住所','eligibility':'希望する人','image':'画像を追加','text':'本文追加','selection_method':'選考方法'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'eligibility': forms.Textarea(attrs={'class': 'form-control'}),
            'text': forms.Textarea({'class':'form-control'}),
            'selection_method': forms.Textarea({'class':'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    """ユーザープロフィール設定フォーム"""
    class Meta:
        current_year = datetime.now().year
        min_year = current_year - 100
        model = Profile
        fields = ['family_name','first_name','sex','birthday','email','postal_code','prefectures','address','career','introduce']
        labels = {'family_name':'姓','first_name':'名前','sex':'性別','birthday':'生年月日','email':'emailアドレス','postal_code':'郵便番号', 'prefuctures':'都道府県', 'address':'都道府県以降の住所', 'career': '以前所属していた企業・役職', 'introduce':'自己PR'}
        widgets = {
            'family_name': forms.TextInput({'class':'form-control'}),
            'first_name': forms.TextInput({'class':'form-control'}),
            'email': forms.TextInput({'class':'form-control'}),
            'postal_code': forms.TextInput({'class':'form-control'}),
            'address': forms.TextInput({'class':'form-control'}),
            'career': forms.TextInput({'class':'form-control'}),
            'introduce': forms.Textarea({'class':'form-control'}),
            
            'birthday':forms.SelectDateWidget(years=[x for x in range(min_year, current_year)]),
            }

class SearchForm(forms.Form):
    keyword = forms.CharField(label='', max_length=50)
    class Meta:
        fields = ['keyword']
        labels = {'keyword':''}
        widgets = {
            'keyword': forms.TextInput(attrs={'class': 'form-control'}),
        }