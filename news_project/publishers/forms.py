from django import forms
from .models import Publisher, PublisherGroup, CollaborationInvitation
from users.models import CustomUser


class PublisherForm(forms.ModelForm):
    '''
    Form to create or update a Publisher.

    :param data: Optional form submission data.
    :return: Validated Publisher model instance.
    '''
    class Meta:
        model = Publisher
        fields = ['name', 'description']


class CollaborationInvitationForm(forms.ModelForm):
    '''
    Form to manage a collaboration invitation.

    :param data: Optional form submission data.
    :return: Validated CollaborationInvitation model instance.
    '''
    class Meta:
        model = CollaborationInvitation
        fields = ['email', 'role', 'accept']


class SendInviteForm(forms.ModelForm):
    '''
    Form to send a collaboration invitation.

    Limits available roles to editor and journalist.

    :param data: Optional form submission data.
    :return: Validated CollaborationInvitation model instance.
    '''
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
    '''
    Form to accept a collaboration invitation.

    :param data: Optional form submission data.
    :return: Boolean indicating whether the invitation was accepted.
    '''
    accept = forms.BooleanField(label="Accept invitation")
