from django.contrib.auth import get_user_model
from rest_framework import serializers

from polls.serializers import ResultUserSerializer

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "results",
        ]

    def get_results(self, obj):
        results = obj.results.all()
        return ResultUserSerializer(results, many=True).data


class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
        ]
