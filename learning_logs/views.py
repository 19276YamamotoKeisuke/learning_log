from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

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
#     objectsは全てのデータを指している→filterでuser選別
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """1つのトピックとそれについての全ての記事を表示"""
    topic = Topic.objects.get(id=topic_id)
    # トピックが現在のユーザーが所持するものであることを確認する
    # if topic.owner != request.user:
    #     raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def entries(request):
    """全ての記事を表示する"""
    entries = Entry.objects.order_by('date_added').reverse()
    context = {'entries': entries}
    return render(request, 'learning_logs/entries.html', context)


@login_required
def entry(request, entry_id):
    """各記事の詳細ページ_topics/entry/<entry_id>で続ける"""
    entry = Entry.objects.get(id=entry_id)
    
    # entry = Entry.object.order_by('date_added')
    context = {'entry': entry}
    return render(request, 'learning_logs/every_entry.html', context)


# @login_required
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
            return redirect('learning_logs:topics')

    # 空または無効のフォームを表示する
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


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



# @login_required
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
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def my_page(request, user_id):
    """マイページ生成"""
    user_id = request.user.id
    entries = Entry.objects.filter(entry_owner=request.user).order_by('date_added')
    context = {'user_id': user_id, 'entries': entries}
    return render(request, 'learning_logs/my_page.html', context)