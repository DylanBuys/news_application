from django import forms
from .models import Article, Newsletter, NewsletterIssue, Comment 


class ArticleForm(forms.ModelForm):
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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class NewsletterForm(forms.ModelForm):
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


class NewsletterIssueForm(forms.ModelForm):
    class Meta:
        model = NewsletterIssue
        fields = ['subject', 'featured_articles', 'is_draft']

        def __init__(self, *args, **kwargs):
            publisher = kwargs.pop('publisher', None)
            super().__init__(*args, **kwargs)
            if publisher:
                self.fields['featured_articles'].queryset = Article.objects.filter(publisher=publisher, status=Article.Status.PUBLISHED)