from rest_framework import viewsets, status
from rest_framework.response import Response

from forum_app.models import Post
from forum_app.serializers import PostSerializer, PostChangeSerializer
from .permissions import IsOwnerOrReadOnly
from ..main_views.utils import create_activity


class PostApiView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        posts = Post.objects.filter(is_active=True)
        user = self.request.user
        if not user.is_authenticated:
            return posts

        queryset = Post.objects.filter(is_active=False, user=self.request.user)
        return (posts | queryset).distinct()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return PostSerializer
        return PostChangeSerializer

    def create(self, request, *args, **kwargs):
        serializer: PostChangeSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if serializer.instance.is_active:
            create_activity(user=request.user,
                            post=serializer.instance,
                            action_type="Пользователь написал новый пост",
                            action_name="new_post")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if not instance.is_active and request.data.get('is_active', False):
            create_activity(user=request.user,
                            post=instance,
                            action_type="Пользователь написал новый пост",
                            action_name="new_post")

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer: PostSerializer = self.get_serializer(instance)
        response_data = serializer.data
        response_data['status'] = "OK"
        try:
            self.perform_destroy(instance)
        except:
            response_data['status'] = "ERROR"

        return Response(response_data)
