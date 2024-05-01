from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(label='Your Answer', max_length=255)