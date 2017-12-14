from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetail.as_view()),
    path('books/<int:book_id>/buy', views.buy_book),
    path('books/bought', views.BoughtByUserBookList.as_view()),
    path('books/top', views.TopBookList.as_view()),
]
