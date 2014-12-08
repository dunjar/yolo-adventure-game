# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext
from django.contrib import admin
from django.conf import settings
from django import forms
from datetime import datetime, timedelta
from quiz.models import *
from django.forms.formsets import all_valid
from django.contrib.admin import helpers
from django.contrib.admin.util import unquote
from django.db import models, transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.encoding import force_unicode

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name','question_count','played')
    prepopulated_fields = {"slug": ("name",)}

    def question_count(self, obj):
        return obj.question_set.count()
    question_count.short_description = _('questions')
    
    def played(self, obj):
        return obj.game_set.count()
    played.short_description = _('games')

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    fieldsets = (
        (None, { 'fields': ('answer','value',)}),
    )

class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)
    inlines = [ AnswerInline, ]

admin.site.register(Quiz, QuizAdmin)    
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Answer)
admin.site.register(Player)


