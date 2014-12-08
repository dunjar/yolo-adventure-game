try:
    from django.conf.urls.defaults import *
except:
    from django.conf.urls import *
from quiz.views import *

urlpatterns = patterns('',
    url(r'^$', quiz_list),
    url(r'^setavatar/$', setavatar),
    url(r'^question/$', get_question),
    url(r'^check/$', check_answer),
    url(r'^(?P<slug>[\-\d\w]+)/$', quiz),
)
