from django.db import models
from users.models import CustomUser
from django.conf import settings


# Create your models here.

class Article(models.Model):
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


class NewsletterIssue(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name='issues')
    subject = models.CharField(max_length=255)
    featured_articles = models.ManyToManyField(Article, related_name='newsletter_issues')
    sent_at = models.DateTimeField(null=True, blank=True)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return f"Issue of {self.newsletter.title} - {self.subject}"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    # replies to other comments
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"
