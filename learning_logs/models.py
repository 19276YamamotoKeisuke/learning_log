from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """モデルの文字列表現を返す"""
        return self.text


class Apply(models.Model):
    """記事と記事への応募関連付け"""
    # entry_id = models.ForeignKey(Entry, on_delete=models.CASCADE)
    # owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    # applicant_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    entry_id = models.CharField(max_length=20)
    owner_id = models.CharField(max_length=20)
    applicant_id = models.CharField(max_length=20)
    # counter = models.SmallIntegerField(default=0)


class Profile(models.Model):
    """ユーザープロフィール"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    postal_code = models.CharField(verbose_name="郵便番号", max_length=10)
    prefectures = models.CharField(verbose_name="都道府県", choices=settings.PREFECTURES, max_length=4)
    address = models.CharField(max_length=30)
    career = models.CharField(max_length=100) #以前所属していた会社&役職
    introduce = models.CharField(max_length=500) #自己紹介&自己PR文

    # def __str__(self):
    #     """モデルの文字列表現を返す"""
    #     return self.user