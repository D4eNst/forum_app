from rest_framework import generics, viewsets
from rest_framework.response import Response

from forum_app.models import CustomUser
from forum_app.serializers import UserSerializer, UserChangeSerializer


class UserApiView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return UserSerializer
        return UserChangeSerializer

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
