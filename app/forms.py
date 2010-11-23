from django import forms

from app import config

class RateResultForm(forms.Form):
    result_id = forms.CharField()
    friend_id = forms.CharField()
    topic_ids = forms.CharField()
    preference = forms.FloatField()

    def clean(self):
        tids = self.cleaned_data['topic_ids']
        tids = [x.strip() for x in tids.split(',')]
        tids = [x for x in tids if x]
        self.cleaned_data['topic_ids'] = tids
        return self.cleaned_data

class ThayResponseForm(forms.Form):
    response_id = forms.CharField(required=False)
    question_id = forms.CharField(required=False)

