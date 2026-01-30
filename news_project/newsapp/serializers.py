from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    '''
    Serializes an Article instance.

    :param instance: Article model instance or queryset to be serialized.
    :return: Serialized Article data.
    '''
    class Meta:
        model = Article
        fields = ['title', 'content', 'author', 'publisher']
