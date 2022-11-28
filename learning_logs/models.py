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
    title = models.CharField(max_length=200)
    eligibility = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to='img/', null=True, blank=True)
    entry_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # title = models.CharField(max_length=200, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """モデルの文字列表現を返す"""
        return self.text


class Apply(models.Model):
    """記事と記事への応募関連付け"""
    entry_id = models.CharField(max_length=20)
    owner_id = models.CharField(max_length=20)
    applicant_id = models.CharField(max_length=20)
    # counter = models.SmallIntegerField(default=0)