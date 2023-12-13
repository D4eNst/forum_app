from rest_framework import serializers
from forum_app.models import CustomUser





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['groups', 'user_permissions']
        read_only_fields = ('last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')


class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
