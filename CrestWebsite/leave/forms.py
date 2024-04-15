from django import forms
from .models import Leave
import datetime

class LeaveCreationForm(forms.ModelForm):
    reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    class Meta:
        model = Leave
        exclude = ['user','defaultdays','hrcomments','status','is_approved','updated','created']

        widgets = {
            'leavetype' : forms.Select(attrs={'class' : 'form-select form-select-lg'}),
            'startdate' : forms.TextInput(attrs={'class' : 'form-select form-select-lg'}),
            'enddate' : forms.TextInput(attrs={'class' : 'form-select form-select-lg'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(LeaveCreationForm, self).__init__(*args, **kwargs)
        self.fields['reason'].widget.attrs['class'] = 'form-control form-select-lg'

    def clean_enddate(self):
        enddate = self.cleaned_data['enddate']
        startdate = self.cleaned_data['startdate']
        today_date = datetime.date.today()
        
        if (startdate or enddate) < today_date:# both dates must not be in the past
            raise forms.ValidationError("Selected dates are incorrect,please select again")
        elif startdate >= enddate:# TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
            raise forms.ValidationError("Selected dates are wrong")
        return enddate