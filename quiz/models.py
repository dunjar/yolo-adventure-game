# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import striptags



class Quiz(models.Model):
    """ A Quiz, what else """
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(_('slug'), max_length=50)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name        = _(u'quiz')
        verbose_name_plural = _(u'quizzes')

class Question(models.Model):
    """ Question model, contains a question and relations to Answers """
    quiz = models.ForeignKey(Quiz)
    question = models.TextField(_('question'))
    questionset = models.ForeignKey('QuestionSet')
    class Meta:
        verbose_name        = _(u'question')
        verbose_name_plural = _(u'questions')
        
    def __unicode__(self):
        return u'%s' % self.question

class Answer(models.Model):
    """ Answer model, contains an answer, a value for the answer, order and is related to a Question """
    value = models.SmallIntegerField(_(u'points'), blank=True, null=True)
    order = models.SmallIntegerField(_(u'order'), blank=True, null=True)
    answer = models.TextField(_('answer'), blank=True)
    question = models.ForeignKey(Question)

    class Meta:
        ordering = ['question', 'order']
        verbose_name        = _(u'answer')
        verbose_name_plural = _(u'answers')
        
    def __unicode__(self):
        return self.answer

class QuestionSet(models.Model):
    """ A set of questions """
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(_('slug'), max_length=50)
    
    def __unicode__(self):
        return self.name

class Player(models.Model):
    """ Player model, with a name, and optionally an User object, holds number of wins """
    name = models.CharField(_('name'), max_length=50)
    user = models.ForeignKey(User, blank=True, null=True)
    wins = models.SmallIntegerField(_(u'wins'), blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
class Game(models.Model):
    step = models.SmallIntegerField(_('step'),default=0)
    quiz = models.ForeignKey(Quiz)
    players = models.ManyToManyField(Player)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    