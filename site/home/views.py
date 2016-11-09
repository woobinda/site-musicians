from django.shortcuts import render
from musicians.models import Musician
from blog.models import Article


def home(request):
    last_musicians = Musician.objects.order_by('-created_date')[:4]
    popular_articles = Article.objects.order_by('-views')[:4]

    return render(request, 'home/index.html', {'title': 'Home',
                                               'last_musicians': last_musicians,
                                               'popular_articles': popular_articles})
