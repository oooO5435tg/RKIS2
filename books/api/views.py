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
        except ValidationError as e:
            if (Book.objects.get(title=request.data['title']).publisher != request.data['publisher'] and request.data[
                'genre'] == 'художественное произведение, переведенное с другого языка'):
                serializer.is_valid()
            if (Book.objects.get(title=request.data['title']).yearofRel != request.data['yearOfRel'] and request.data[
                'genre'] == 'учебник'):
                serializer.is_valid()
            else:
                raise ValidationError(self.errors)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AuthorCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AuthorSerializer
