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
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


def signup(request):
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
    if request.user.role != 'journalist':
        return redirect('users:journalist_homepage')
    return render(request, 'homepage_journalist.html')


def reader_homepage(request):
    if request.user.role != 'reader':
        return redirect('users:reader_homepage')
    return render(request, 'homepage_reader.html')


def editor_homepage(request):
    if request.user.role != 'editor':
        return redirect('users:editor_homepage')
    return render(request, 'editor_homepage.html')


def logout_user(request):
    logout(request)
    return redirect("users:login")


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def checkout_success(request):
    return render(request, 'checkout_success.html')


@login_required
def sub_to_journalist(request, pk):
    user = request.user
    journalist = CustomUser.objects.get(role='journalist', pk=pk)
    user.subscribed_journalists.add(journalist)
    return redirect('users:profile_view')


def unsub_to_journalist(request, pk):
    user = request.user
    journalist = get_object_or_404(CustomUser, pk=pk, role='journalist')
    user.subscribed_journalists.remove(journalist)
    return redirect('users:profile_view')


@login_required
def sub_to_publisher(request, pk):
    user = request.user
    publisher = get_object_or_404(Publisher, pk=pk)
    user.subscribed_publishers.add(publisher)
    return redirect('users:profile_view')


def unsub_to_publisher(request, pk):
    user = request.user
    publisher = get_object_or_404(Publisher, pk=pk)
    user.subscribed_publishers.remove(publisher)
    return redirect('users:profile_view')


@login_required
def toggle_subscription(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    user = request.user
    
    if publisher in user.subscribed_publishers.all():
        user.subscribed_publishers.remove(publisher)
    else:
        user.subscribed_publishers.add(publisher)
        
    return redirect('publisher_detail', pk=pk)


def password_reset(request):
    return PasswordResetView.as_view()(request)


def password_reset_done(request):
    return PasswordResetDoneView.as_view()(request)


def password_reset_confirm(request, uidb64, token):
    return PasswordResetConfirmView.as_view()(request, uidb64=uidb64, token=token)


def password_reset_complete(request):
    return PasswordResetCompleteView.as_view()(request)
