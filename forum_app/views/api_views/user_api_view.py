from rest_framework import viewsets
from rest_framework.response import Response

from forum_app.models import CustomUser
from forum_app.serializers import UserSerializer, UserChangeSerializer
from forum_app.views.api_views.permissions import IsOwnerOrReadOnly


class UserApiView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserChangeSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        response_data['status'] = "OK"
        try:
            self.perform_destroy(instance)
        except:
            response_data['status'] = "ERROR"

        return Response(response_data)
