from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry, Apply, Profile, User, Recommend
from .forms import TopicForm, EntryForm, ProfileForm, SearchForm, ApplyForm, RecommendForm

# Create your views here.
def index(request):
    """学習ノートのホームページ"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """全てのトピックを表示する"""
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    # objectsは全てのデータを指している→filterでuser選別
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """1つのトピックとそれについての全ての記事を表示"""
    topic = Topic.objects.get(id=topic_id)
    form = SearchForm(request.GET)
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        entries = Entry.objects.filter(text__icontains = keyword).order_by('date_added').reverse
    else:
        form = SearchForm()
        entries = Entry.objects.order_by('date_added').reverse()
        
    context = {'topic': topic,'entries': entries, 'form': form}
    return render(request, 'learning_logs/entries.html', context)
    # topic = Topic.objects.get(id=topic_id)
    # # トピックが現在のユーザーが所持するものであることを確認する
    # # if topic.owner != request.user:
    # #     raise Http404

    # entries = topic.entry_set.order_by('-date_added')
    # context = {'topic': topic, 'entries': entries}
    # return render(request, 'learning_logs/topic.html', context)


@login_required
def entries(request):
    """全ての記事を表示する"""
    #仮実装 エラー出るので要改良→ルックアップでできた
    form = SearchForm(request.GET)
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        entries = Entry.objects.filter(text__icontains = keyword).order_by('date_added').reverse
    else:
        form = SearchForm()
        entries = Entry.objects.order_by('date_added').reverse()
        
    context = {'entries': entries, 'form': form}
    return render(request, 'learning_logs/entries.html', context)


@login_required
def users(request):
    """全てのユーザーを表示する"""
    form = SearchForm(request.GET)
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        users = Profile.objects.filter(introduce__icontains = keyword)
    else:
        form = SearchForm()
        users = Profile.objects.all()
        
    context = {'users': users, 'form': form}
    return render(request, 'learning_logs/users.html', context)
    # users = Profile.objects.all()
    # context = {'users':users}
    # return render(request, 'learning_logs/users.html', context)


@login_required
def entry(request, entry_id):
    """各記事の詳細ページ_topics/entry/<entry_id>で続ける"""
    entry = Entry.objects.get(id=entry_id)
    
    # entry = Entry.object.order_by('date_added')
    context = {'entry': entry}
    return render(request, 'learning_logs/every_entry.html', context)


@login_required
def new_topic(request):
    """新規トピックを追加する"""
    if request.method != 'POST':
        #データは送信されていないので空のフォームを生成する
        form = TopicForm()

    else:
        # POSTでデータが送信されたのでこれを処理する
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # 新しく追加したトピックを現在のユーザーと紐づける
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # form.save()
            return redirect('learning_logs:new_entry')

    # 空または無効のフォームを表示する
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def edit_Profile(request, user_id):
    """プロフィール初期設定"""
    profile = Profile.objects.get(id=user_id)

    if request.method != 'POST':
        form = ProfileForm(instance=profile)
    
    else:
        #送信されたデータの処理
        form = ProfileForm(data=request.POST)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            return redirect('learning_logs:my_page',user_id)
    
    context = {'form': form}
    return render(request, 'learning_logs/edit_profile.html', context)


@login_required
def new_entry(request):
    """新規記事を追加する"""
    # topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # データは送信されなかったので空のフォームを生成する
        form = EntryForm()
        # image_form = UploadForm()

    else:
        # POSTでデータが送信されたのでこれを処理する
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.entry_owner = request.user
            new_entry.save()
            
            return redirect('learning_logs:entries')

    # 空または無効のフォームを送信する
    context = {'form': form}
    return render(request, 'learning_logs/new_entry.html', context)



@login_required
def edit_entry(request, entry_id):
    """既存の記事を編集する"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # ログイン制限かけるやつ
    # if topic.owner != request.user:
    #     raise Http404

    if request.method != 'POST':
        # 初回リクエスト時は現在の記事の内容がフォームに埋め込まれている
        form = EntryForm(instance=entry)

    else:
        # POSTでデータが送信されたのでこれを処理する
        form = EntryForm(request.POST,request.FILES,instance=entry)
        if form.is_valid():
            # form.save()
            new_entry = form.save(commit=False)
            new_entry.save()
            return redirect('learning_logs:entry',entry_id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def edit_Profile(request, user_id):
    """プロフィール初期設定"""
    
    if Profile.objects.filter(user=user_id).exists():
        profile = Profile.objects.get(user=user_id)
        print('え')

    if request.method != 'POST':
        if Profile.objects.filter(user=user_id).exists():
            form = ProfileForm(instance=profile)
            print('あ')
        else:
            form = ProfileForm()
            print('い')
    
    else:
        #送信されたデータの処理
        if Profile.objects.filter(user=user_id).exists():
            form = ProfileForm(data=request.POST, instance=profile)
        else:
            form = ProfileForm(data=request.POST)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            return redirect('learning_logs:my_page',user_id)
    
    context = {'form': form}
    return render(request, 'learning_logs/edit_profile.html', context)


@login_required
def my_page(request, user_id):
    """マイページ生成"""
    # user_id = request.user.id
    entries = Entry.objects.filter(entry_owner=request.user).order_by('-date_added')
    applys = Apply.objects.filter(owner_id=user_id)
    entry_applied = Apply.objects.filter(applicant_id=user_id)
    if Profile.objects.filter(user=user_id).exists():
        profile = Profile.objects.get(user=user_id)
    else:
        profile = ''
    recommend = Recommend.objects.filter(user=user_id)

    context = {'user_id': user_id, 'entries': entries, 'applys':applys, 'entry_applied':entry_applied, 'profile':profile, 'recommend':recommend}
    return render(request, 'learning_logs/my_page.html', context)


@login_required
def other_page(request, applicant_id):
    """他ユーザーの情報を閲覧できるページ"""
    s_id = applicant_id
    user = User.objects.get(username=s_id)
    # この方法しか今のとこ無理だけどusername重複した場合は？→重複しなかった(アカウント登録画面で弾かれた)
    profile = Profile.objects.get(user=user.id)
    # apply = Apply.objects.get(id=apply_id)
    context = {'profile':profile}

    return render(request, 'learning_logs/other_users_page.html', context)


@login_required
def other_page2(request, applicant_id):
    """他ユーザーの情報を閲覧できるページ"""
    s_id = applicant_id
    user = User.objects.get(username=s_id)
    # この方法しか今のとこ無理だけどusername重複した場合は？→重複しなかった(アカウント登録画面で弾かれた)
    profile = Profile.objects.get(user=user.id)
    # apply = Apply.objects.get(id=apply_id)
    context = {'profile':profile}

    return render(request, 'learning_logs/other_users_page2.html', context)


@login_required
def apply_entry(request, entry_id, user_id):
    """応募確認ページ"""
    entry = Entry.objects.get(id=entry_id)
    if request.method != 'POST':
        form = ApplyForm()
    
    else:
        #送信されたデータの処理
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            apply = form.save(commit=False)
            # apply = Apply(entry_id=entry, owner_id=entry.entry_owner, applicant_id=request.user)
            apply.entry_id = entry
            apply.owner_id = entry.entry_owner
            apply.applicant_id = request.user
            apply.save()
            context = {'entry_id':entry_id, 'user_id':user_id, 'entry':entry}
            return redirect('learning_logs:apply_entered', user_id, entry_id)

    context = {'form':form, 'entry_id':entry_id, 'user_id':user_id, 'entry':entry}
    return render(request, 'learning_logs/apply_entry.html',  context)
    #応募機能仮完成→応募最終確認のページ作成へ


@login_required
def recommend(request, profile_user):
    """応募確認ページ"""
    name = profile_user
    user = User.objects.get(username=name)
    profile = Profile.objects.get(user=user.id)
    if request.method != 'POST':
        form = RecommendForm()
    
    else:
        # if request.user != entry.
        #送信されたデータの処理
        form = RecommendForm(request.POST)
        if form.is_valid():
            recommend = form.save(commit=False)
            # recommend.owner_id = request.user
            recommend.user_id = user.id
            recommend.save()
            # context = {'entry_id':entry_id, 'user_id':user_id, 'entry':entry}
            return redirect('learning_logs:other_page', profile.user)

    context = {'form':form, 'profile':profile}
    return render(request, 'learning_logs/recommend.html',  context)


@login_required
def apply_entered(request, user_id, entry_id):
    """応募完了"""
    # entry = Entry.objects.get(id=entry_id)
    # owner = User.objects.get(id=entry.entry_owner)
    # user = User.objects.get(id=user_id)
    # form = Apply(entry_id=entry, owner_id=entry.entry_owner, applicant_id=request.user)
    # form.save()
    # context = {'entry_id':entry_id, 'user_id':user_id}
    return render(request, 'learning_logs/apply_entered.html')
