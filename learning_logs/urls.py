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
    # 全ての記事を表示するページ
    path('topics/entries/', views.entries, name='entries'),
    # 個別トピックの詳細ページ
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # 個別記事の詳細ページ
    path('topics/entries/<int:entry_id>', views.entry, name='entry'),
    # 新規トピックの追加ページ
    path('new_topic/', views.new_topic, name='new_topic'),
    # 新規記事の追加ページ
    path('new_entry/', views.new_entry, name='new_entry'),
    # 記事の編集ページ
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # マイページ
    path('my_page/<int:user_id>', views.my_page, name='my_page'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)