from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from .models import Book
from .serializers import BookShortForAnonSerializer, BookShortForAuthorizedSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('name', 'authors__name', 'authors__surname')
    search_fields = ('name', 'authors__name', 'authors__surname')

    def get_serializer_class(self):
        if self.request.user.is_anonymous:
            return BookShortForAnonSerializer
        return BookShortForAuthorizedSerializer
