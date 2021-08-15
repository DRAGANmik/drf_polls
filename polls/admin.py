from django.contrib import admin

from .models import Answer, AnswerItem, Poll, Question, QuestionItem, Result


class AnswerItemAdmin(admin.ModelAdmin):
    model = AnswerItem
    filter_horizontal = ("answers",)


class AnswerItemThroughAdmin(admin.TabularInline):
    model = Result.answers.through
    extra = 0


class AnswerAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    model = QuestionItem


class QuestionItemAdmin(admin.StackedInline):
    model = QuestionItem
    extra = 0


class PollAdmin(admin.ModelAdmin):
    inlines = (QuestionItemAdmin,)


class ResultAdmin(admin.ModelAdmin):
    inlines = [AnswerItemThroughAdmin]
    list_display = ["id", "poll", "user", "session_id"]
    fields = ("poll", "user", "session_id")


admin.site.register(AnswerItem, AnswerItemAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Poll, PollAdmin)
