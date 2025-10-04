from django import forms
from .models import Ticket, Comment

class DateInput(forms.DateInput):
    input_type = 'date'

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'due_date', 'status']
        widgets = {
            'due_date': DateInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
