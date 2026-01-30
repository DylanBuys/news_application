from django.db import models
from django.conf import settings
from users.models import CustomUser


class Publisher(models.Model):
    '''
    Model representing a publisher entity.

    :param name: Name of the publisher.
    :param description: Optional description of the publisher.
    :param owner: User who owns this publisher (one-to-one relationship).
    :param members: Users who are members of this publisher.
    '''
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # 1-to-1: Only one User can be the Owner of this specific Publisher
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_publisher',
        limit_choices_to={'role': 'EDITOR'},
    )

    # 1-to-Many: Multiple users can be "staff" for this publisher.
    # ManyToManyField because a User might also belong to multiple publishers.
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PublisherMember',
        related_name='joined_publishers'
    )

    def __str__(self):
        return self.name


class PublisherGroup(models.Model):
    '''
    Model representing a grouping of staff members for a publisher.

    :param publisher: Related Publisher instance.
    '''
    publisher = models.ForeignKey('publishers.Publisher', null=True, blank=True, on_delete=models.SET_NULL, related_name='staff_members')


class PublisherMember(models.Model):
    '''
    Intermediate model representing a user’s membership in a publisher.

    :param user: User who is a member of the publisher.
    :param publisher: Publisher the user belongs to.
    :param date_joined: Date and time when the user joined the publisher.
    '''
    """ Intermediate model to store extra info about the membership (like roles) """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)


class CollaborationInvitation(models.Model):
    '''
    Model representing an invitation to collaborate with a publisher.

    :param email: Email address of the invited user.
    :param publisher: Publisher issuing the invitation.
    :param role: Role assigned to the invited user.
    :param token: Unique token used to validate the invitation.
    :param created_at: Timestamp when the invitation was created.
    :param accept: Indicates whether the invitation has been accepted.
    '''
    email = models.EmailField()
    publisher = models.ForeignKey('publishers.Publisher', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=CustomUser.ROLE_CHOICES)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation for {self.email} to join {self.publisher.name} as {self.role}"


# publishers/models.py
class JoinRequest(models.Model):
    '''
    Model representing a request by a user to join a publisher.

    :param user: User requesting to join.
    :param publisher: Publisher the user wants to join.
    :param created_at: Timestamp when the request was created.
    :param approved: Indicates whether the request has been approved.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'publisher')

    def __str__(self):
        return f"{self.user} → {self.publisher}"
