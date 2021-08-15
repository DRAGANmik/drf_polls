from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Answer, AnswerItem, Poll, Question, QuestionItem, Result


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    choices = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = "__all__"

    def validate(self, data):
        data_type = data["type"]
        choices = data.get("choices")
        if data_type != "text" and choices is None:
            raise serializers.ValidationError("Нужно ввести вопросы")
        if choices is None:
            data["choices"] = []
        return data

    def create(self, validated_data):
        choices = validated_data.pop("choices")
        poll_pk = self.context.get("poll_pk")
        poll = get_object_or_404(Poll, pk=poll_pk)
        choices_list = [
            Answer.objects.create(answer=item["answer"]) for item in choices
        ]
        question = Question.objects.create(**validated_data)
        poll.questions.add(question)
        for item in choices_list:
            question.choices.add(item)

        return validated_data

    def update(self, instance, validated_data):
        choices = validated_data.pop("choices")
        question = Question.objects.filter(id=instance.id)
        question.update(**validated_data)
        instance_choices_list = [choice for choice in instance.choices.all()]

        instance.choices.remove(*instance_choices_list)

        for choice in choices:
            choice = Answer.objects.create(answer=choice["answer"])
            instance.choices.add(choice)

        return instance


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = "__all__"

    def update(self, instance, validated_data):
        start_at_old = instance.start_at
        start_at_new = validated_data.get("start_at")
        if start_at_old != start_at_new:
            raise serializers.ValidationError("Нельзя менять дату начала")

        return validated_data


class ResultPostSerializer(serializers.ModelSerializer):
    answers = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(), many=True, required=False
    )
    text_answer = serializers.CharField(max_length=500, required=False)
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )

    class Meta:
        model = Result
        fields = ["answers", "question", "text_answer"]

    def validate(self, data):
        request = self.context.get("request")
        poll_pk = self.context.get("poll_pk")
        poll = get_object_or_404(Poll, pk=poll_pk)
        question = data["question"]
        try:
            text_answer = data["text_answer"]
            answers = []
        except KeyError:
            text_answer = ""
            answers = data.get("answers")

        question_item = get_object_or_404(
            QuestionItem, question=question, poll=poll
        )

        if (
            len(answers) < 1
            and question.type != "text"
            or len(text_answer) < 1
            and question.type == "text"
        ):
            raise serializers.ValidationError("Нужен ответ")
        elif len(answers) > 1 and len(text_answer) > 1:
            raise serializers.ValidationError("Проверьте типы ответов")

        if question.type != "text":
            for answer in answers:
                if answer not in question.choices.all():
                    raise serializers.ValidationError("Неверный ответ")

        if request.user.id:
            result = Result.objects.filter(user=request.user)
        else:
            result = Result.objects.filter(
                session_id=request.session.session_key
            )

        result = AnswerItem.objects.filter(
            question_item=question_item, result__in=result
        )
        if result.exists():
            raise serializers.ValidationError("Уже отвечали")

        if question.type == "one" and len(answers) > 1:
            raise serializers.ValidationError("Нужен только один ответ")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        answers = validated_data.get("answers")
        text_answer = validated_data.get("text_answer")

        if not request.session.session_key:
            request.session.save()
        poll_pk = self.context.get("poll_pk")
        poll = get_object_or_404(Poll, pk=poll_pk)

        question = validated_data["question"]
        question_item = QuestionItem.objects.get(question=question, poll=poll)

        answers_item = AnswerItem.objects.create(question_item=question_item)
        if question.type == "text":
            answer = Answer.objects.create(answer=text_answer)
            answers_item.answers.add(answer)
        else:
            answers_item.answers.add(*answers)

        result, created = Result.objects.get_or_create(
            poll=poll, session_id=request.session.session_key
        )
        result.answers.add(answers_item)

        if request.user.id:
            result.user = request.user
            result.save()
        return validated_data


class AnswerItemSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    question = serializers.SerializerMethodField()

    class Meta:
        model = AnswerItem
        fields = ["id", "question", "answers"]

    def get_question(self, obj):
        return QuestionSerializer(obj.question_item.question).data


class ResultUserSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = ["id", "poll", "answers"]

    def get_answers(self, obj):
        qs = AnswerItem.objects.filter(question_item__poll=obj.poll)
        return AnswerItemSerializer(qs, many=True).data
