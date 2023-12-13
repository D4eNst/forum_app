from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from forum_app.models import Comment
from forum_app.serializers import CommentSerializer, CommentChangeSerializer
from .permissions import IsOwnerOrReadOnly


class CommentApiView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'create', 'retrieve']:
            return CommentSerializer
        return CommentChangeSerializer

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
