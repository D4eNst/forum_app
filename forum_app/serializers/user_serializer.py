from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from forum_app.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_active']
        read_only_fields = ('last_login', 'is_staff', 'date_joined')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class UserChangeSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        password = make_password(validated_data['password'])
        validated_data['password'] = password
        return super(UserSerializer, self).create(validated_data)
