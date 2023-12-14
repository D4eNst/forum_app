from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from forum_app.models import Comment
from forum_app.serializers import CommentSerializer, CommentChangeSerializer
from .permissions import IsOwnerOrReadOnly
from ..main_views.utils import create_activity


class CommentApiView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'create', 'retrieve']:
            return CommentSerializer
        return CommentChangeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        create_activity(user=request.user,
                        post=serializer.instance.post,
                        action_type="Пользователь прокомментировал пост",
                        action_name="comments")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        response_data['updated_at'] = timezone.now()
        response_data['status'] = "OK"
        try:
            self.perform_destroy(instance)
        except:
            response_data['status'] = "ERROR"

        return Response(response_data)
