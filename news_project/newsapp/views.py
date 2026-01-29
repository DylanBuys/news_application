import tweepy

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleForm, NewsletterForm
from users.models import CustomUser
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Article, Newsletter
from publishers.models import Publisher
from publishers.views import join_requests
from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ArticleSerializer


def announce_article_on_x(article_id):
    # Validating the article object.
    try:
        article = Article.objects.select_related().get(id=article_id)
    except Article.DoesNotExist:
        return
    client = tweepy.Client(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET,
        access_token=settings.TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
    )
    # Image settings.
    # auth = tweepy.OAuth1UserHandler(consumer_key=settings.TWITTER_API_KEY, consumer_secret=settings.TWITTER_API_SECRET, access_token=settings.TWITTER_ACCESS_TOKEN, access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
    # v1_api = tweepy.API(auth)
    # media = v1_api.media_upload(store.cover_page.path)

    # X post (tweet).
    client.create_tweet(text=f"New Article Added: {article.title}")


@login_required
def create_article(request):
    '''
    View to create a new article.
    :param request: HTTP request object.
    :return: Rendered template for creating a new article.
    '''
    if request.method == "POST":
        form = ArticleForm(request.POST, user=request.user)
        if form.is_valid():
            article = form.save(commit=False)

            # Always set the author
            article.author = request.user

            # Attach publication if the journalist belongs to one
            publishers = request.user.joined_publishers.all()
            if publishers.exists():
                article.publisher = publishers.first()
            else:
                # Independent journalist
                article.publisher = None
                # article.independent_author.set(request.user)

            # Force safe defaults
            # article.status = "pending"        # Never published automatically
            # article.is_approved = False     # Never approved automatically

            article.save()
            article.independent_author.add(request.user)
            return redirect("newsapp:article_list")
    else:
        form = ArticleForm(user=request.user)

    return render(request, "articles/article_form.html", {"form": form})


@login_required
def article_list(request):
     '''
    This view will display a list of articles/newsletters

        :param request: HTTP object
        :return: Rendered template with a list of articles/newsletters
    '''
    articles = Article.objects.filter(is_approved=True)
    newsletters = Newsletter.objects.filter(is_approved=True)

    context = {
        "articles": articles,
        "newsletters": newsletters,
        "page_title": "All Articles"
    }

    return render(request, "articles/article_list.html", context)


@login_required
def article_detail(request, pk):
    '''
    View to display details of a specific article.
    :param request: HTTP request object.
    :param pk: Primary key of the article.
    :return: Rendered template with details of the specified article.
    '''
    article = get_object_or_404(Article, pk=pk)
    context = {
        "article": article
    }
    return render(request, "articles/article_detail.html", context)


@login_required
def article_update(request, pk):
    '''
    View to update an existing article.
    :param request: HTTP request object.
    :param pk: Primary key of the article to be updated.
    :return: Rendered template for updating the specified article.
    '''

    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article, user=request.user)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect("newsapp:article_list")
    else:
        form = ArticleForm(instance=article, user=request.user)
    return render(request, "articles/article_form.html", {"form": form})


@login_required
def article_delete(request, pk):
    '''
    View to delete an existing article.
    :param request: HTTP request object.
    :param pk: Primary key of the article to be deleted.
    :return: Redirect to the article list after deletion.
    '''

    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect("newsapp:article_list")


@login_required
def newsletter_createf(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST, user=request.user)
        if form.is_valid():
            newsletter = form.save(commit=False)

            # Always set the author
            newsletter.author = request.user

            # Attach publication if the journalist belongs to one
            publishers = request.user.joined_publishers.all()
            if publishers.exists():
                newsletter.publisher = publishers.first()
            else:
                # Independent journalist
                newsletter.publisher = None
                newsletter.independent_author = request.user

            # Force safe defaults
            newsletter.status = "PENDING REVIEW"        # Never published automatically
            newsletter.is_approved = False     # Never approved automatically

            newsletter.save()
            return redirect("newsapp:article_list")
    else:
        form = NewsletterForm(user=request.user)

    return render(request, "newsletter/newsletter_form.html", {"form": form})


@login_required
def newsletter_create(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST, user=request.user)
        if form.is_valid():
            newsletter = form.save(commit=False)

            # Always set the author
            newsletter.author = request.user

            # Attach publication if the journalist belongs to one
            publishers = request.user.joined_publishers.all()
            if publishers.exists():
                newsletter.publisher = publishers.first()
            else:
                # Independent journalist
                newsletter.publisher = None
                # article.independent_author.set(request.user)

            newsletter.save()
            newsletter.independent_author.add(request.user)
            return redirect("newsapp:article_list")
    else:
        form = ArticleForm(user=request.user)

    return render(request, "articles/article_form.html", {"form": form})


def newsletter_list(request):
    if request.user.role == 'reader':
        newsletters = Newsletter.objects.filter(is_approved=True)
    else:
        newsletters = Newsletter.objects.all()

        context = {
            "newsletters": newsletters,
            "page_title": "All newsletters"
        }

        return render(request, "newsletters/newsletter_list.html", context)


@login_required
@user_passes_test(lambda u: u.role == 'editor')
def newsletter_update(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.journalist = request.user
            newsletter.publisher = request.publisher
            form.save()
        return redirect("newsletters: newsletter_list")
    else:
        form = NewsletterForm()
    return render(request, "newsletters/newsletter_form.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.role == 'editor')
def newsletter_delete(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.delete()
    return redirect("newsletters: newsletter_list")


def newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    context = {
        "newsletter": newsletter
    }
    return render(request, "newsletters/newsletter_detail.html", context)


def approve_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.user.role == 'editor':
        newsletter.is_approved = True
        newsletter.save()
    return redirect('newsletters:newsletter_list')


def reject_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.user.role == 'editor':
        newsletter.is_approved = False
        newsletter.save()
    return redirect('newsletters:newsletter_list')


def approve_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.role == 'editor':
        article.is_approved = True
        # announce_article_on_x(article_id=article.id)
        article.save()
    return redirect('newsapp:article_list')


@login_required
def index(request):
    articles = Article.objects.filter(is_approved=True).order_by('-id')[:5]
    newsletters = Newsletter.objects.filter(is_approved=True).order_by('-id')[:5]

    context = {
        "articles": articles,
        "newsletters": newsletters,
        "page_title": "Latest News",
        "user_role": request.user.role,
        "user_subscribed_publishers": request.user.subscribed_publishers.all(),
        "user_subscribed_journalists": request.user.subscribed_journalists.all(),
    }
    return render(request, 'newsapp/index.html', context)


def my_projects(request):
    articles = Article.objects.filter(is_approved=True).order_by('-id')[:5]
    newsletters = Newsletter.objects.filter(is_approved=True).order_by('-id')[:5]

    my_projects = {
        "articles": Article.objects.filter(journalist=request.user),
        "newsletters": Newsletter.objects.filter(journalist=request.user),
    }
    context = {
        "articles": articles,
        "newsletters": newsletters,
        "page_title": "My Projects",
        "my_projects": my_projects,
    }
    return render(request, 'newsapp/my_projects.html', context)


def join_publisher(request, pk):
    user = request.user
    publisher = get_object_or_404(Publisher, pk=pk)
    user.subscribed_publishers.add(publisher)
    return redirect('newsapp:index')


def reader_dasboard(request):
    return render(request, 'newsapp: reader_dashboard')


def publisher_dashboard(request):
    return render(request, 'newsapp/publisher_dashboard')


@login_required
def editor_dashboard(request):

    if request.user.role != 'editor':
        return redirect('newsapp:dashboard')

    # Get ONE publisher instance
    publisher = request.user.joined_publishers.first()

    pending_articles = Article.objects.filter(
        publisher=publisher,
        status='pending'
    ).order_by('-created_at')

    # staff_members = publisher.members.all()
    articles = Article.objects   #filter(publisher=publisher)

    context = {
        'publisher': publisher,          # ✅ real model instance
        'pending_articles': pending_articles,
        # 'members': staff_members,
        'articles': articles,
    }

    return render(request, 'publishers/dashboard.html', context)


@login_required
def journalist_dashboard(request):
    if request.user.role != 'journalist':
        return redirect('newsapp:editor_dashboard')

    publishers = request.user.joined_publishers.all()
    my_articles = Article.objects.filter(author=request.user).order_by('-created_at')

    # Only show pending articles in their publishers, not written by themselves
    pending_articles = Article.objects.filter(
        publisher__in=publishers,
        status='PENDING'
    ).exclude(author=request.user).order_by('-created_at')

    context = {
        'publishers': publishers,
        'my_articles': my_articles,
        'pending_articles': pending_articles
    }

    return render(request, 'publishers/journalist_dashboard.html', context)


@login_required
def reader_dashboard(request):
    user = request.user

    context = {
        "subscribed_journalists": user.subscribed_journalists.all(),
        "subscribed_publishers": user.subscribed_publishers.all(),
    }

    return render(request, "publishers/reader_dashboard.html", context)


@login_required
def dashboard(request):
    """
    Redirects the user to the appropriate dashboard based on their role.
    Assumes you have defined these names in your urls.py.
    """
    user = request.user

    if user.role == 'reader':
        return redirect('newsapp:reader_dashboard')
    elif user.role == 'journalist':
        return redirect('newsapp:journalist_dashboard')
    else:
        # Default for editors or other roles
        return redirect('newsapp:editor_dashboard')


def workspace(request):
    '''
    View for editors to access the publication drafts
    and active edits.
    '''
    # Article must also belong to same publisher group
    articles = Article.objects.filter(is_approved=False)
    context = {
        "articles": articles,
        "page_title": "Draft Articles"
    }
    return render(request, "newsapp/workspace.html", context)


@login_required
def subscribe(request, pk):
    if request.method != "POST":
        return HttpResponseForbidden("Invalid request method.")

    article = get_object_or_404(Article, pk=pk)

    if request.user.role != "reader":
        return HttpResponseForbidden("Only readers can subscribe.")

    if article.publisher:
        request.user.subscribed_publishers.add(article.publisher)
    else:
        request.user.subscribed_journalists.add(article.author)

    return redirect("newsapp:confirm_subscription", pk=pk)


@login_required
def confirm_subscription(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user.role != "reader":
        return HttpResponseForbidden("Only readers can subscribe.")

    if article.publisher:
        target = article.publisher
        target_type = "publisher"
    else:
        target = article.author
        target_type = "journalist"

    # return render(
    #     request,
    #     "newsapp/confirm_subscription.html",
    #     {
    #         "article": article,
    #         "target": target,
    #         "target_type": target_type,
    #     }
    # )
    return redirect("newsapp:reader_dashboard")


# Unsubscribe from a journalist
@login_required
def unsub_to_journalist(request, pk):
    if request.method != "POST":
        return HttpResponseForbidden("Invalid request method.")

    journalist = get_object_or_404(CustomUser, pk=pk, role="journalist")
    request.user.subscribed_journalists.remove(journalist)

    return redirect("newsapp:reader_dashboard")


# Unsubscribe from a publisher
@login_required
def unsub_to_publisher(request, pk):
    if request.method != "POST":
        return HttpResponseForbidden("Invalid request method.")

    publisher = get_object_or_404(Publisher, pk=pk)
    request.user.subscribed_publishers.remove(publisher)

    return redirect("newsapp:reader_dashboard")


@api_view(['GET'])
def subscribed_articles(request, pk):
    user = CustomUser.objects.get(id=pk)
    publisher_articles = Article.objects.filter(publisher__in=user.subscribed_publishers.all())
    journalist_articles = Article.objects.filter(author__in=user.subscribed_journalists.all())
    articles = publisher_articles | journalist_articles
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

# For more information on implementing Role-Based Access Control (RBAC) in Django, refer to:
# https://python.plainenglish.io/how-to-implement-role-based-access-control-rbac-in-django-a-step-by-step-guide-31c5e4053868

# invoice
# https://www.geeksforgeeks.org/python/setup-sending-email-in-django-project/
