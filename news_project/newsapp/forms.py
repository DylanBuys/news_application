from django import forms
from .models import Article, Newsletter


class ArticleForm(forms.ModelForm):
    '''
    Form for creating and updating Article objects.
    Fields:
    - title: CharField for the title.
    - content: CharField for the content.
    - author: CharField for the author of article.

    Meta class:
    - Defines the model to use (Article) and the fields to include in the
    form.
    :param forms.ModelForm: Django's ModelForm class.
    '''
    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pass request.user
        super().__init__(*args, **kwargs)

        if user and user.role == "journalist":

            publishers = user.joined_publishers.all()

            if publishers.exists():
                # Journalist in a publication
                for field in ["is_approved"]:
                    self.fields.pop(field)

                self.fields.pop("publisher")
                self.fields["status"].choices = [
                    ("draft", "DRAFT"),
                    ("pending", "PENDING REVIEW"),
                ]
            else:
                # Independent journalist
                for field in ["publisher"]:
                    self.fields.pop(field)

                self.fields["status"].choices = [
                    ("draft", "DRAFT"),
                ]


class NewsletterForm(forms.ModelForm):
    '''
    Form for creating and updating Newsletter objects.
    Fields:
    - title: CharField for the title.
    - description: CharField for the content.
    - subject: CharField for the author of newsletter.

    Meta class:
    - Defines the model to use (Newsletter) and the fields to include in the
    form.
    :param forms.ModelForm: Django's ModelForm class.
    '''
    class Meta:
        model = Newsletter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pass request.user
        super().__init__(*args, **kwargs)

        if user and user.role == "journalist":

            publishers = user.joined_publishers.all()

            if publishers.exists():
                # Journalist in a publication
                for field in ["is_approved"]:
                    self.fields.pop(field)

                self.fields.pop("publisher")
                self.fields["status"].choices = [
                    ("draft", "DRAFT"),
                    ("pending", "PENDING REVIEW"),
                ]
            else:
                # Independent journalist
                for field in ["publisher"]:
                    self.fields.pop(field)

                self.fields["status"].choices = [
                    ("draft", "DRAFT"),
                ]
