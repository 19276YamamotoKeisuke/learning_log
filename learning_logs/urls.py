"""learning_logsのURLパターンの定義"""

from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'learning_logs'
urlpatterns = [
    #ホームページ
    path('', views.index, name='index'),
    # すべてのトピックを表示するページ
    path('topics/', views.topics, name = 'topics'),
    # 個別トピックの詳細ページ
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # 新規トピックの追加ページ
    path('new_topic/', views.new_topic, name='new_topic'),
    # 新規記事の追加ページ
    path('new_entry/<int:topic_id>/', views.new_entry, name = 'new_entry'),
    # 記事の編集ページ
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # 画像用
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)