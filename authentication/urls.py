from django.urls import path

from .views import index, article


urlpatterns = [
path('', index, name="authentication-index"),
path('article-<str:num_article>/', article, name="authentication-article")
]