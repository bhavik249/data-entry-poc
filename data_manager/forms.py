
from django import forms
 
from .models import Events
# creating a form
class BulkCreateEventForm(forms.Form):
    title = forms.FileField()

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = "__all__"
        widgets = {'date': forms.DateInput(format='%d/%m/%Y')}