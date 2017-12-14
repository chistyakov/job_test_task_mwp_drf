from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Book
from .serializers import (
    BookShortForAnonSerializer, BookShortForAuthorizedSerializer,
    BookDetailForAnonSerializer, BookDetailForAuthorizedSerializer,
)
from .services import serve_book_buying


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('name', 'authors__name', 'authors__surname')
    search_fields = ('name', 'authors__name', 'authors__surname')

    def get_serializer_class(self):
        if self.request.user.is_anonymous:
            return BookShortForAnonSerializer
        return BookShortForAuthorizedSerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_anonymous:
            return BookDetailForAnonSerializer
        return BookDetailForAuthorizedSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def buy_book(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)
    card_name = request.data.get('card_name')
    # TODO: replace with async request to the payment gateway with status push/polling
    serve_book_buying(book, user, card_name)
    return Response(status=status.HTTP_200_OK)


class BoughtByUserBookList(generics.ListAPIView):
    serializer_class = BookShortForAuthorizedSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.profile.bought_books.all()


class TopBookList(generics.ListAPIView):
    serializer_class = BookShortForAnonSerializer

    def get_queryset(self):
        return Book.objects.annotate(num_sold=Count('buyers')).order_by('-num_sold')

    # TODO: replace with schedule-based caching to fit requirements
    #       (celery beat task + redis)
    @method_decorator(cache_page(60 * 60 * 24))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
