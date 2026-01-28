from django.urls import path
from .views import (
    send_invitation,
    create_publication,
    send_invite,
    request_join,
    view_invitations,
    accept_invite
)

app_name = 'publishers'

urlpatterns = [
    path('invite/', send_invitation, name='send_invitation'),

    path('publishers/create_publication/', create_publication, name='create_publication'),

    path('publishers/send_invite/<int:pk>/', send_invite, name="send_invite"),

    path('send_invitation/<int:pk>/', send_invitation, name="send_invitation"),

    # publishers/urls.py
    path("invitations/", view_invitations, name="view_invitations"),

    # publishers/urls.py
    path("request-join/", request_join, name="request_join"),

    path("accept-invite/<str:token>/", accept_invite, name="accept_invite"),
]
