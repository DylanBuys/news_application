from django import forms
from .models import Publisher, PublisherGroup, CollaborationInvitation
from users.models import CustomUser


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'description']


class CollaborationInvitationForm(forms.ModelForm):
    class Meta:
        model = CollaborationInvitation
        fields = ['email', 'role', 'accept']


class SendInviteForm(forms.ModelForm):
    class Meta:
        model = CollaborationInvitation
        fields = ["email", "role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].choices = [
            choice for choice in CustomUser.ROLE_CHOICES
            if choice[0] in ["editor", "journalist"]
        ]


class AcceptInviteForm(forms.Form):
    accept = forms.BooleanField(label="Accept invitation")
