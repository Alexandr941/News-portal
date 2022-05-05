from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Autor(models.Model):
    autorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    raitingAutor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRaiting=Sum('raiting'))
        pRat = 0
        pRat += postRat.get('postRaiting')

        commentRat = self.autorUser.comment_set.aggregate(commentRaiting=Sum('raiting'))
        cRat = 0
        cRat += commentRat.get('commentRaiting')

        self.raitingAutor = pRat *3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Autor, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    raiting = models.SmallIntegerField(default=0)

    def like(self):
        self.raiting +=1
        self.save()

    def dislike(self):
        self.raiting -=1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    postThrought = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrought = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    raiting = models.SmallIntegerField(default=0)

    def like(self):
        self.raiting += 1
        self.save()

    def dislike(self):
        self.raiting -= 1
        self.save()
