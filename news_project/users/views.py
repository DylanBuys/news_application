from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import UserForm
from django.contrib.auth.views import (PasswordResetView, 
                                       PasswordResetDoneView, 
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from publishers.models import Publisher


def user_list(request):
    '''
    View to list all users.

    :param request: HTTP request object.
    :return: Renders a template with all CustomUser instances.
    '''
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


def signup(request):
    '''
    View to register a new user and log them in.

    :param request: HTTP request object.
    :return: Renders the signup form or redirects to role-specific dashboard
            after successful signup.
    '''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()  # Now user has an ID

            # Now it's safe to modify many-to-many fields
            if user.role in ['journalist', 'editor']:
                user.subscribed_publishers.clear()
                user.subscribed_journalists.clear()

            form.save_m2m()  # Save other M2M data from the form

            auth_login(request, user)
            request.session['username'] = user.id
            request.session['role'] = user.role
            request.session.set_expiry(300)
            if user.role == 'reader':
                return redirect('newsapp:reader_dashboard')
            elif user.role == 'journalist':
                return redirect('newsapp:journalist_dashboard')
            elif user.role == 'editor':
                return redirect('newsapp:editor_dashboard')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    '''
    View to log in an existing user.

    :param request: HTTP request object.
    :return: Authenticates the user and redirects to their role-specific dashboard,
            or renders login page with an error if credentials are invalid.
    '''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['username'] = user.id  # Add username to session
            request.session['role'] = user.role   # Add user role to session
            request.session.set_expiry(1800)  # session expires in 30 minutes

            if user.role == 'editor':
                return redirect("newsapp:editor_dashboard")
            elif user.role == 'journalist':
                return redirect("newsapp:journalist_dashboard")
            elif user.role == 'reader':
                return redirect("newsapp:reader_dashboard")
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')


def journalist_homepage(request):
    '''
    View to display the journalist's homepage.

    :param request: HTTP request object.
    :return: Renders the journalist homepage template or redirects if the user is not a journalist.
    '''
    if request.user.role != 'journalist':
        return redirect('users:journalist_homepage')
    return render(request, 'homepage_journalist.html')


def reader_homepage(request):
    '''
    View to display the reader's homepage.

    :param request: HTTP request object.
    :return: Renders the reader homepage template or redirects if the user is not a reader.
    '''
    if request.user.role != 'reader':
        return redirect('users:reader_homepage')
    return render(request, 'homepage_reader.html')


def editor_homepage(request):
    '''
    View to display the editor's homepage.

    :param request: HTTP request object.
    :return: Renders the editor homepage template or redirects if the user is not an editor.
    '''
    if request.user.role != 'editor':
        return redirect('users:editor_homepage')
    return render(request, 'editor_homepage.html')


def logout_user(request):
    '''
    View to log out the current user.

    :param request: HTTP request object.
    :return: Logs out the user and redirects to the login page.
    '''
    logout(request)
    return redirect("users:login")


@login_required
def profile(request):
    '''
    View to display the profile of the logged-in user.

    :param request: HTTP request object.
    :return: Renders the profile template with the current user.
    '''
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def checkout_success(request):
    '''
    View to display a success page after a checkout.

    :param request: HTTP request object.
    :return: Renders the checkout success template.
    '''
    return render(request, 'checkout_success.html')


@login_required
def sub_to_journalist(request, pk):
    '''
    View to subscribe the logged-in user to a journalist.

    :param request: HTTP request object.
    :param pk: Primary key of the journalist to subscribe to.
    :return: Redirects to the user's profile view.
    '''
    user = request.user
    journalist = CustomUser.objects.get(role='journalist', pk=pk)
    user.subscribed_journalists.add(journalist)
    return redirect('users:profile_view')


def unsub_to_journalist(request, pk):
    '''
    View to unsubscribe the logged-in user from a journalist.

    :param request: HTTP request object.
    :param pk: Primary key of the journalist to unsubscribe from.
    :return: Redirects to the user's profile view.
    '''
    user = request.user
    journalist = get_object_or_404(CustomUser, pk=pk, role='journalist')
    user.subscribed_journalists.remove(journalist)
    return redirect('users:profile_view')


@login_required
def sub_to_publisher(request, pk):
    '''
    View to subscribe the logged-in user to a publisher.

    :param request: HTTP request object.
    :param pk: Primary key of the publisher to subscribe to.
    :return: Redirects to the user's profile view.
    '''
    user = request.user
    publisher = get_object_or_404(Publisher, pk=pk)
    user.subscribed_publishers.add(publisher)
    return redirect('users:profile_view')


def unsub_to_publisher(request, pk):
    '''
    View to unsubscribe the logged-in user from a publisher.

    :param request: HTTP request object.
    :param pk: Primary key of the publisher to unsubscribe from.
    :return: Redirects to the user's profile view.
    '''
    user = request.user
    publisher = get_object_or_404(Publisher, pk=pk)
    user.subscribed_publishers.remove(publisher)
    return redirect('users:profile_view')


@login_required
def toggle_subscription(request, pk):
    '''
    View to toggle subscription status of a publisher for the logged-in user.

    :param request: HTTP request object.
    :param pk: Primary key of the publisher.
    :return: Adds or removes the publisher from the user's subscriptions
            and redirects to the publisher detail page.
    '''
    publisher = get_object_or_404(Publisher, pk=pk)
    user = request.user
    
    if publisher in user.subscribed_publishers.all():
        user.subscribed_publishers.remove(publisher)
    else:
        user.subscribed_publishers.add(publisher)
        
    return redirect('publisher_detail', pk=pk)


def password_reset(request):
    '''
    View to start the password reset process.

    :param request: HTTP request object.
    :return: Calls Django's PasswordResetView.
    '''
    return PasswordResetView.as_view()(request)


def password_reset_done(request):
    '''
    View to show password reset done page.

    :param request: HTTP request object.
    :return: Calls Django's PasswordResetDoneView.
    '''
    return PasswordResetDoneView.as_view()(request)


def password_reset_confirm(request, uidb64, token):
    '''
    View to confirm a password reset using the token.

    :param request: HTTP request object.
    :param uidb64: Encoded user ID from the password reset email.
    :param token: Password reset token.
    :return: Calls Django's PasswordResetConfirmView.
    '''
    return PasswordResetConfirmView.as_view()(request, uidb64=uidb64, token=token)


def password_reset_complete(request):
    '''
    View to show password reset completion page.

    :param request: HTTP request object.
    :return: Calls Django's PasswordResetCompleteView.
    '''
    return PasswordResetCompleteView.as_view()(request)
