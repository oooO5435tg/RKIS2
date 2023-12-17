from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView)

urlpatterns = [
    path('books', BookListView.as_view()),
    path('books/<int:pk>', BookDetailListView.as_view()),
    path('books/create', BookCreateView.as_view()),

    path('authors/<int:pk>', AuthorDetailListView.as_view()),
    path('authors/create', AuthorCreateView.as_view()),

    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
