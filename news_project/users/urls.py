from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    signup,
    login,
    logout_user,
    profile,
    reader_homepage,
    journalist_homepage,
    editor_homepage,
    sub_to_publisher,
    sub_to_journalist,
    unsub_to_journalist,
    unsub_to_publisher
)

app_name = 'users'

urlpatterns = [
    # URL pattern for displaying signup view
    path("", signup, name="signup"),

    # URL pattern for displaying login_view
    path("login", login, name="login"),

    # URL pattern for loggin out user
    path("logout", logout_user, name="logout_user"),


    # URL pattern for displaying profile
    path("profile/", profile, name="profile"),

    # URL pattern for displaying password_reset view
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'
    ), name='password_reset'),

    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ),  name='password_reset_complete'),

    path('reader-homepage/', reader_homepage, name='reader_homepage'),
    path('journalist-homepage/', journalist_homepage, name='journalist_homepage'),
    path('editor-homepage/', editor_homepage, name='editor_homepage'),

    # subscription paths
    path('subscribe/journalist/<int:pk>/', sub_to_journalist, name='sub_to_journalist'),
    path('subscribe/publisher/<int:pk>/', sub_to_publisher, name='sub_to_publisher'),

    path('unsubscribe/journalist/<int:pk>/', unsub_to_journalist, name='unsub_to_journalist'),
    path('unsubscribe/publisher/<int:pk>/', unsub_to_publisher, name='unsub_to_publisher'),
]
