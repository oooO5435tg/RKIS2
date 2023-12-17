from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError


class AuthorDetailListView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookDetailListView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'genre', 'author']


class BookCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            if self.is_duplicate_book(request.data):
                return Response({'error': 'Дублирующая книга'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            raise ValidationError(e)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def is_duplicate_book(self, data):
        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')

        existing_books = Book.objects.filter(title=title, author=author, genre=genre)

        if genre == 'художественное произведение, переведенное с другого языка':
            publisher = data.get('publisher')
            existing_books = existing_books.filter(publisher=publisher)

        if genre == 'учебник':
            year_of_release = data.get('yearOfRel')
            existing_books = existing_books.filter(yearOfRel=year_of_release)

        return existing_books.exists()


class AuthorCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AuthorSerializer
