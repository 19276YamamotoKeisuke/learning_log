from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm, UploadForm

# Create your views here.
def index(request):
    """学習ノートのホームページ"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """全てのトピックを表示する"""
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
#     objectsは全てのデータを指している→filterでuser選別
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """1つのトピックとそれについての全ての記事を表示"""
    topic = Topic.objects.get(id=topic_id)
    # トピックが現在のユーザーが所持するものであることを確認する
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


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
            return redirect('learning_logs:topics')

    # 空または無効のフォームを表示する
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """特定のトピックに新規記事を追加する"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # データは送信されなかったので空のフォームを生成する
        form = EntryForm()
        image_form = UploadForm()

    else:
        # POSTでデータが送信されたのでこれを処理する
        form = EntryForm(data=request.POST)
        image_form = UploadForm(data=request.POST)
        if form.is_valid() and image_form.is_valid():
            # form_get_image = image_form.save(commit=False)
            new_entry = image_form.save(commit=False)
            # new_entry = form_get_image
            new_entry.topic = topic
            new_entry.save()
            # upload_image = image_form.save(commit=False)
            # upload_image.save()
            
            return redirect('learning_logs:topic', topic_id=topic_id)

    # 空または無効のフォームを送信する
    context = {'topic': topic, 'form': form, 'image_form':image_form }
    return render(request, 'learning_logs/new_entry.html', context)



@login_required
def edit_entry(request, entry_id):
    """既存の記事を編集する"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # ログイン制限かけるやつ
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初回リクエスト時は現在の記事の内容がフォームに埋め込まれている
        form = EntryForm(instance=entry)

    else:
        # POSTでデータが送信されたのでこれを処理する
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)