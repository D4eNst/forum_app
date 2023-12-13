from rest_framework import serializers

from forum_app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('likes',)

        # extra_kwargs = {
        #     'likes': {'read_only': True}
        # }


class CommentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'user', 'post', 'created_at']


class CommentChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('likes', 'post', 'user')
