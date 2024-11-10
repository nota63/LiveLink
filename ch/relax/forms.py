from django import forms 
from.models import Invite
from accounts.models import CustomUser

class InviteForm(forms.ModelForm):
    users=forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model=Invite
        fields='__all__'

      # Override the label to display first name only
    def __init__(self, *args, **kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        self.fields['users'].label_from_instance = lambda obj: obj.first_name    
