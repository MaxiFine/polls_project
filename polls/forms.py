from django import forms
from .models import Polls



class PollsQueationForm(forms.ModelForm):
    class Meta:
        model = Polls
        fields = ['question', 'option1', 'option2', 'option3',]


class SharePollForm(forms.Form):
    # name = forms.CharField(max_length=50, blank=True)
    email = forms.EmailField()
    to = forms.EmailField()
    #comments = forms.CharField(required=False, widget=forms.Textarea)


class EditPollForm(forms.ModelForm):
    class Meta:
        model = Polls
        fields = ['question', 'author', 'option1',
                  'option2','option3', 'status',]

