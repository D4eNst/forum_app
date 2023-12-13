from rest_framework import viewsets
from rest_framework.response import Response

from forum_app.models import Post
from forum_app.serializers import PostSerializer, PostChangeSerializer
from .permissions import IsOwnerOrReadOnly


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
