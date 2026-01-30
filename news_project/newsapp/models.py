from django.db import models
from users.models import CustomUser
from django.conf import settings


# Create your models here.


class Article(models.Model):
    '''
    Model representing an Article

    Fields:
    -title: charfield with a max length of 255
    -content: textfield with no max limit
    -status: charfield with a max length of 20, choices=draft, pending, 
                published, rejected, default choice=draft
    -is_approved: boleanfield, default=Flase
    -created_at: Dtae time field, auto_add
    -updated_at: Dtae time field, auto_add

    Relationships:
    -author: 
    -publisher
    Methods:
    __str__: Returns a string representation of the article, showing
    the title

    :param models.Model: Django's base model class.
    '''
    class Status(models.TextChoices):
    
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending Review'
        PUBLISHED = 'published', 'Published'
        REJECTED = 'rejected', 'Rejected'
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_approved = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles')
    publisher = models.ForeignKey('publishers.Publisher', on_delete=models.CASCADE, related_name='articles', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    '''
    Model representing an Article

    Fields:
    -title: charfield with a max length of 255
    -description: textfield with no max length
    -subject: textfield with no max limit
    -status: charfield with a max length of 20, choices=draft, pending, 
                published, rejected, default choice=draft
    -is_approved: boleanfield, default=Flase
    -created_at: Dtae time field, auto_add
    -updated_at: Dtae time field, auto_add
    -is_active: booleanfield, default=True

    Relationships:
    -author
    -publisher
    Methods:
    __str__: Returns a string representation of the article, showing
    the title

    :param models.Model: Django's base model class.
    '''
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending Review'
        PUBLISHED = 'published', 'Published'
        REJECTED = 'rejected', 'Rejected'
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=255, blank=True)
    publisher = models.ForeignKey('publishers.Publisher', on_delete=models.CASCADE, related_name='newsletters', null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_approved = models.BooleanField(default=False)

    receive_this_specific_newsletter_subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='subscribed_newsletters',
        blank=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.publisher.name}"
