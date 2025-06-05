from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField("title", max_length=200)
    slug = models.SlugField(
        "slug",
        unique=True,
    )
    description = models.TextField("description")


class Post(models.Model):
    text = models.TextField("text")
    pub_date = models.DateTimeField("publication date", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    image = models.ImageField("photo", upload_to="posts/", blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
    )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField("text")
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="outgoing",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="incoming",
    )
