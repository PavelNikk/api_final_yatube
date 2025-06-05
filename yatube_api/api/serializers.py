from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "text", "created")
        read_only_fields = ("post",)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Post
        fields = ("id", "text", "author", "pub_date", "image", "group")


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
    )

    class Meta:
        model = Follow
        fields = ("user", "following")

    def validate(self, data):
        source = self.context["request"].user
        destination = data.get("following")
        if source == destination:
            raise serializers.ValidationError("Fail")
        if Follow.objects.filter(user=source, following=destination).exists():
            raise serializers.ValidationError("Sub already exists")
        return data
