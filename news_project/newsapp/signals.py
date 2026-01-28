import tweepy


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Article, Newsletter
from users.models import CustomUser


@receiver(post_save, sender=Article)
def email_subscribers_on_publish(sender, instance, created, **kwargs):

    # Check if the article is approved/published
    if instance.is_approved:  # of is_approved=True
        # Subscribers list
        print("[SIGNAL] Article is published, sending emails...")
        if instance.publisher:
            # All users subscribed to this publisher
            subscribers = CustomUser.objects.filter(
                subscribed_publishers=instance.publisher
            )
            print("[SIGNAL] Article is published, sending emails...")
        else:
            # All users subscribed to independent journalist
            subscribers = CustomUser.objects.filter(
                subscribed_journalists=instance.author
            )

        subject = f"New Article: {instance.title}"
        message = f"Hi!\n\nA new article has been published: {instance.title}\nCheck it out at: https:localhost"

        for user in subscribers:
            if not user.email:
                print(f"[SIGNAL] Skipping {user.username}: no email")
                continue

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                print(f"[SIGNAL] Email successfully sent to {user.email}")
            except Exception as e:
                print(f"[SIGNAL] ERROR sending email to {user.email}: {e}")


@receiver(post_save, sender=Newsletter)
def email_subscribers_on_newsletter(sender, instance, created, **kwargs):
    if instance.is_approved:  # Only send when published
        print(f"[SIGNAL] Newsletter '{instance.title}' is approved, sending emails...")

        # Determine subscribers
        if instance.publisher:
            subscribers = CustomUser.objects.filter(subscribed_publishers=instance.publisher)
        else:
            subscribers = CustomUser.objects.filter(subscribed_journalists=instance.author)

        subject = f"New Newsletter: {instance.title}"
        message = (
            f"Hi!\n\nA new newsletter has been published: {instance.title}\n"
            # f"Check it out here: http://yourdomain.com/newsletters/{instance.pk}"
            f"Check it out here: http: https:https:localhost"
        )

        for user in subscribers:
            if not user.email:
                print(f"[SIGNAL] Skipping {user.username}: no email")
                continue

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                print(f"[SIGNAL] Email successfully sent to {user.email}")
            except Exception as e:
                print(f"[SIGNAL] ERROR sending email to {user.email}: {e}")


@receiver(post_save, sender=Article)
def announce_article_on_x(sender, instance, **kwargs):
    # Only post when approved
    if not instance.is_approved:
        return

    client = tweepy.Client(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET,
        access_token=settings.TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
    )

    client.create_tweet(
        text=f"New Article Added: {instance.title}, by: {instance.author}"
    )
