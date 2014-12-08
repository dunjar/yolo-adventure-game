from django.forms import ModelForm
from quiz.models import *

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ('name',)
