from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Reader-specific fields
    subscribed_publishers = models.ManyToManyField('publishers.Publisher', blank=True, related_name='reader_subscribers')
    subscribed_journalists = models.ManyToManyField('users.CustomUser', blank=True, symmetrical=False, related_name='follower_readers')

    # Journalist-specific fields (Independent work)
    independent_articles = models.ManyToManyField('newsapp.Article', blank=True, related_name='independent_author')
    independent_newsletters = models.ManyToManyField('newsapp.Newsletter', blank=True, related_name='independent_author')

    publisher_group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL, related_name='publisher_users')
