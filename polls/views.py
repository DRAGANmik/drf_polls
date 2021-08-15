from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Poll
from .permissions import IsPollAdmin
from .serializers import (
    PollSerializer,
    QuestionSerializer,
    ResultPostSerializer,
)


class PollViewSet(ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.filter(end_at__gt=timezone.now())
    permission_classes = [IsPollAdmin]

    @action(
        detail=True,
        methods=["POST"],
        url_path="answer",
        url_name="poll-answer",
        serializer_class=ResultPostSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def poll_answer(self, request, pk):
        """Answer to poll
        If question type is text then "answers" field must be emtpy.
        For this type need to use field "text_answer".
        Otherwise exclude "text_answer" field from request.
        """

        serializer = self.serializer_class(
            data=request.data, context={"request": request, "poll_pk": pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsPollAdmin]

    def get_serializer_context(self):
        return {"poll_pk": self.kwargs.get("poll_pk")}

    def get_queryset(self):
        poll_pk = self.kwargs.get("poll_pk")
        poll = get_object_or_404(Poll, pk=poll_pk)
        return poll.questions.all()
