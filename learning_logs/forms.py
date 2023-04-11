from django import forms
from .models import Topic, Entry
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {"text" : ""}
        widgets = {"text": forms.TextInput(attrs={"placeholder": "Enter the title"})}
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {"text" : ""}
        widgets = {'text' : forms.Textarea(attrs={'cols' : 80, "placeholder" : "Enter more than 250 words"})}