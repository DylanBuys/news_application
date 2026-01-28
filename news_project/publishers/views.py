import uuid
import secrets

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PublisherForm, CollaborationInvitationForm, SendInviteForm, AcceptInviteForm
from .models import Publisher, CollaborationInvitation, JoinRequest
from newsapp.models import Article, Newsletter
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def create_publication(request):
    # Check if user already owns a publication
    if Publisher.objects.filter(owner=request.user).exists():
        messages.error(request, "You already own a publication. You cannot create another one.")
        return redirect("newsapp:editor_dashboard")

    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():  # ✅ fixed
            publisher = form.save(commit=False)
            publisher.main_editor = request.user
            publisher.owner = request.user  # ✅ safer than setting owner_id manually
            publisher.save()

            # ✅ add creator to members M2M
            publisher.members.add(request.user)

            return redirect("newsapp:editor_dashboard")  # ✅ fixed typo
    else:
        form = PublisherForm()

    return render(request, "publishers/publisher_form.html", {"form": form})


def send_invitation(request):
    if request.user.role != 'editor':
        return redirect('home')

    if request.method == 'POST':
        form = CollaborationInvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.publisher = request.user.managed_publisher
            invitation.token = uuid.uuid4().hex
            invitation.save()
            # Here you would typically send an email with the invitation token
            return redirect('publisher_dashboard')
    else:
        form = CollaborationInvitationForm()

    return render(request, 'publishers/invite_form.html', {'form': form})


# Inside your CollaborationInvitation model:
def generate_token(self):
    if not self.token:
        # Generate a secure 64-character token
        self.token = secrets.token_urlsafe(48)
    return self.token


def send_invitation_email(self, request):
    # Construct the full URL for the user to click
    accept_url = request.build_absolute_uri(
        reverse('accept-invitation', kwargs={'token': self.token})
    )

    subject = f"Invite to join {self.publisher.name} on our platform"
    message = f"You have been invited to join {self.publisher.name} as a {self.role}.\n\nClick here to join: {accept_url}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [self.email],
        fail_silently=False,
    )


@login_required
def send_invite(request, pk):
    # Get the publisher instance
    publisher = get_object_or_404(Publisher, pk=pk)

    # Only allow editors of this publisher to send invites
    if request.user not in publisher.members.all():
        messages.error(request, "You are not allowed to send invites for this publisher.")
        return redirect('newsapp:editor_dashboard')

    if request.method == 'POST':
        form = SendInviteForm(request.POST)
        if form.is_valid():
            invite = form.save(commit=False)
            invite.publisher = publisher
            invite.token = secrets.token_urlsafe(32)  # generate a unique token
            invite.save()
            messages.success(request, f"Invitation sent to {invite.email}!")
            return redirect('newsapp:editor_dashboard')
    else:
        form = SendInviteForm()

    return render(request, 'publishers/invite_form.html', {'form': form, 'publisher': publisher})


@login_required
def accept_invite(request, token):
    invite = get_object_or_404(
        CollaborationInvitation,
        token=token,
        accept=False
    )

    # Safety check: email must match logged-in user
    if invite.email != request.user.email:
        messages.error(request, "This invitation was not sent to your email.")
        return redirect("newsapp:journalist_dashboard")

    # Add user to publisher
    invite.publisher.members.add(request.user)

    # Update user role if needed
    request.user.role = invite.role
    request.user.save()

    # Mark invite as accepted
    invite.accept = True
    invite.save()

    messages.success(
        request,
        f"You have joined {invite.publisher.name} as a {invite.role.title()}."
    )

    return redirect("newsapp:journalist_dashboard")


@login_required
def request_join(request):
    publishers = Publisher.objects.all()

    if request.method == "POST":
        publisher_id = request.POST.get("publisher_id")
        publisher = get_object_or_404(Publisher, id=publisher_id)

        JoinRequest.objects.get_or_create(
            user=request.user,
            publisher=publisher
        )

        messages.success(
            request,
            f"Join request sent to {publisher.name}"
        )
        return redirect("newsapp:journalist_dashboard")

    return render(
        request,
        "publishers/request_join.html",
        {"publishers": publishers}
    )


@login_required
def join_requests(request):
    publisher = get_object_or_404(Publisher, editors=request.user)

    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")

        join_request = get_object_or_404(
            JoinRequest,
            id=request_id,
            publisher=publisher,
            status="pending"
        )

        if action == "approve":
            join_request.status = "approved"
            join_request.save()

            publisher.journalists.add(join_request.user)

            messages.success(
                request,
                f"{join_request.user} approved."
            )

        elif action == "reject":
            join_request.status = "rejected"
            join_request.save()

            messages.info(
                request,
                f"{join_request.user} rejected."
            )

        return redirect("newsapp:join_requests")

    # GET: wys net pending requests vir daardie publisher
    join_requests = JoinRequest.objects.filter(
        publisher=publisher,
        status="pending"
    )

    return render(
        request,
        "publishers/join_requests.html",
        {"join_requests": join_requests}
    )


@login_required
def view_invitations(request):
    invitations = CollaborationInvitation.objects.filter(
        email=request.user.email,
        accept=False
    )

    return render(
        request,
        "publishers/view_invitations.html",
        {"invitations": invitations}
    )
