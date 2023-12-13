from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from forum_app.models import Category
from forum_app.serializers import CategorySerializer

from forum_app.views.main_views.utils import filter_category
from .permissions import IsOwnerOrReadOnly


class CategoryApiView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]

    def get_queryset(self):
        return filter_category(user=self.request.user)

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

