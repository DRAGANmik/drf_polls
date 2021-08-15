from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from polls.models import Result
from polls.serializers import ResultUserSerializer

from .permissions import IsUserAdmin
from .serializers import UserDetailSerializer, UserSerializer

User = get_user_model()


class ListRetrieveViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    pass


class UserViewSet(ListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserAdmin]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return super().get_serializer_class()

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        url_path="me",
        url_name="me",
    )
    def view_me(self, request):
        """
        Endpoint "me" shows request user info and
        all results from answered poll.
        Also can edit personal data if user is authenticated.
        If user a guest will show only poll results.
        """

        if request.user.id:
            serializer = UserDetailSerializer(request.user, data=request.data)

            if serializer.is_valid() and request.method == "PATCH":
                serializer.save()
            serializer = UserDetailSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        guest = request.session.session_key
        result = Result.objects.filter(session_id=guest)
        serializer = ResultUserSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
