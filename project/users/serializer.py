from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

import helpers


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            user = helpers.create_user(validated_data['username'],
                                       validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }
