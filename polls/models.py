from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Poll(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    questions = models.ManyToManyField("Question", through="QuestionItem")

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"
        ordering = ["id"]

    def __str__(self):
        return self.title


class Question(models.Model):
    TEXT = "text"
    MULTIPLE_CHOICE = "multiple"
    ONE_CHOICE = "one"
    TYPE = [
        (TEXT, "Text"),
        (MULTIPLE_CHOICE, "Multiple choice"),
        (ONE_CHOICE, "One choice"),
    ]
    question = models.TextField()
    type = models.CharField(max_length=8, choices=TYPE, default=ONE_CHOICE)
    choices = models.ManyToManyField("Answer", blank=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["id"]

    def __str__(self):
        return self.question


class QuestionItem(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="questions"
    )
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="polls"
    )

    class Meta:
        verbose_name = "Вопрос опроса"
        verbose_name_plural = "Вопросы опроса"
        ordering = ["poll"]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "poll"], name="unique_poll_item"
            )
        ]

    def __str__(self):
        return "вопрос id {} опрос {}".format(
            self.question.id, self.poll.title
        )


class AnswerItem(models.Model):
    question_item = models.ForeignKey(
        QuestionItem, on_delete=models.CASCADE, related_name="answers"
    )
    answers = models.ManyToManyField("Answer")

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"

    def __str__(self):
        return "Ответы для связки: вопрос id {} опрос {}".format(
            self.question_item.question.id, self.question_item.poll.title
        )


class Answer(models.Model):
    answer = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.answer


class Result(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="results"
    )
    session_id = models.CharField(max_length=32, null=True)
    answers = models.ManyToManyField(AnswerItem)
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="results"
    )

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "poll"], name="unique_result"
            )
        ]
