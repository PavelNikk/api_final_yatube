from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Follow, Group, Post
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from api.permissions import AuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get("post_id"))

    def get_queryset(self):
        return self.get_post().comments

    def perform_create(self, serializer):
        serializer.save(post=self.get_post(), author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FollowViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
