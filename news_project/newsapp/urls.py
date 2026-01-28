from django.urls import path
from .views import (
    create_article,
    dashboard,
    article_list,
    editor_dashboard,
    journalist_dashboard,
    approve_article,
    article_detail,
    article_update,
    article_delete,
    reader_dashboard,
    confirm_subscription,
    subscribe,
    unsub_to_journalist,
    unsub_to_publisher,
    newsletter_detail,
    newsletter_create,
    newsletter_update,
    newsletter_delete,
    subscribed_articles,
)

app_name = 'newsapp'

urlpatterns = [
    path('create/', create_article, name='create_article'),

    path('', dashboard, name='dashboard'),

    path('editor_dashboard/', editor_dashboard, name='editor_dashboard'),

    path('journalist/dashboard', journalist_dashboard, name="journalist_dashboard"),

    path('reader/dashboard/', reader_dashboard, name="reader_dashboard"),

    path('articles/article_list', article_list, name='article_list'),

    path('article/detail/<int:pk>/', article_detail, name='article_detail'),

    path('articles/update/<int:pk>/', article_update, name="article_update"),

    path('articles/delete/<int:pk>', article_delete, name="article_delete"),

    path("subscribe/confirm/<int:pk>/", confirm_subscription, name="confirm_subscription"),

    path("subscribe/<int:pk>/", subscribe, name="subscribe"),

    # path("subscribe/", subscribe, name="subscribe"),

    path('unsub/publisher/<int:pk>/', unsub_to_publisher, name="unsub_to_publisher"),

    path('unsub/journalist/<int:pk>/', unsub_to_journalist, name='unsub_to_journalist'),

    path('newsletter/detail', newsletter_detail, name='newsletter_detail'),

    path('newsletter/create', newsletter_create, name='newsletter_create'),

    path('newsletter/update', newsletter_update, name='newsletter_update'),

    path('newsletter/delete', newsletter_delete, name='newsletter_delete'),

    path('articles/approve/<int:pk>/', approve_article, name="approve_article"),

    path('api/subscribed-articles/<int:pk>/', subscribed_articles, name='subscribed-articles'),
]
