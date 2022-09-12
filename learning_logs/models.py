from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """ユーザーが学んでいるトピックを表す"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     print("サーバー稼働時に呼び出される？")

    def __str__(self):
        """モデルの文字列表現を返す"""
        return self.text


class Entry(models.Model):
    """トピックに関して学んだ具体的なこと"""
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    # image = models.ImageField(upload_to='img/', null=True, blank=True)
    # title = models.CharField(max_length=200, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """モデルの文字列表現を返す"""
        return f"{self.text[:25]}..."


class UploadImage(models.Model):
    """画像保存データベースtest"""
    # entry = models.ForeignKey(Entry, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='img/', null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title