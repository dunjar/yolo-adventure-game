from django.http import HttpResponse,HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from datetime import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
import collections
from random import sample
import json

from quiz.models import *
from quiz.forms import *

def quiz_list(request):
    object_list = Quiz.objects.all()
    
    c = RequestContext(request,{
        'object_list'       : object_list,
    })
    t = template = loader.get_template('quiz/index.html')
    return HttpResponse(t.render(c))

def quiz(request, slug):
    obj = get_object_or_404(Quiz, slug=slug)
    if not request.session.get('playerID',None):
        return playersetup(request,slug)
    player = Player.objects.get(id=request.session.get('playerID'))
    questions = sample(Question.objects.filter(quiz=obj).order_by('?'),5)
    c = RequestContext(request,{
        'questions' : [int(q.id) for q in questions],
        'player': player,
        'avatar' : request.session.get('avatar'),
    })
    t = template = loader.select_template(['quiz/%s/quiz.html' % obj.slug,'quiz/quiz.html'])
    return HttpResponse(t.render(c))

def playersetup(request, slug):
    obj = get_object_or_404(Quiz, slug=slug)
    if request.POST:
        form = PlayerForm(request.POST)
        if form.is_valid():
            player, created = Player.objects.get_or_create(**form.cleaned_data)
            request.session['playerID'] = player.id
            return quiz(request, slug)
    else:
        form = PlayerForm()
    c = RequestContext(request,{
        'quiz' : obj,
        'form' : form, 
    })
    t = template = loader.select_template(['quiz/%s/playersetup.html' % obj.slug,'quiz/playersetup.html'])
    return HttpResponse(t.render(c))
    
def get_question(request):
    qid = request.GET.get('qid')
    if not qid:
        return HttpResponseBadRequest()
    question = Question.objects.get(id=int(qid))
    response = {}
    response['id'] = question.id
    response['question'] = question.question
    response['set'] = question.questionset.slug
    response['answers'] = []
    for answer in question.answer_set.all():
        response['answers'].append({"id": answer.id, "text":answer.answer})
    return HttpResponse(json.dumps(response), content_type="application/json")

def check_answer(request):
    aid = request.GET.get('aid')
    if not aid:
        return HttpResponseBadRequest()
    answer = Answer.objects.get(id=aid)
    response = {}
    response['score'] = answer.value
    return HttpResponse(json.dumps(response), content_type="application/json")

def setavatar(request):
    aurl = request.GET.get('aurl')
    if not aurl:
        return HttpResponseBadRequest()
    request.session['avatar'] = aurl
    return HttpResponse()

    
    

    
    