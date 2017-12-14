import os

import requests
from requests import RequestException
from rest_framework.exceptions import APIException

from .models import Card


class BookAlreadyBought(APIException):
    status_code = 409
    default_detail = 'The book already bought by the user.'
    default_code = 'already_bought'


class InvalidCardName(APIException):
    status_code = 400
    default_detail = 'Invalid card name'
    default_code = 'invalid_card_name'


class PaymentServiceUserError(APIException):
    status_code = 400
    default_detail = 'Payment failed.'
    default_code = 'payment_failed'


class PaymentServiceInternalError(APIException):
    status_code = 500
    default_detail = 'Payment failed on server side.'
    default_code = 'payment_failed_on_server_side'


def serve_book_buying(book, user, card_name):
    card = get_card_or_error(user, card_name)
    if check_book_already_bought(book, user):
        raise BookAlreadyBought
    payment_result = withdraw_money(card.payment_number, book.price)
    if not payment_result:
        raise PaymentServiceUserError
    add_book_to_profile(book, user)


def get_card_or_error(user, card_name):
    try:
        card = user.profile.cards.get(name=card_name)
    except Card.DoesNotExist as e:
        available_cards = [c.name for c in Card.objects.filter(owner=user.profile)]
        raise InvalidCardName(detail=f'Invalid card name. Available cards: {available_cards}') from e
    return card


def check_book_already_bought(book, user):
    return user.profile.bought_books.filter(pk=book.id).exists()


def withdraw_money(payment_number, amount):
    try:
        response = requests.post(os.environ.get('PAYMENT_GETWAY_URL'),
                                 json={'pan': payment_number, 'amount': str(amount)})
        response.raise_for_status()
    except RequestException as e:
        raise PaymentServiceInternalError from e
    return response.json().get('success', False)


def add_book_to_profile(book, user):
    user.profile.bought_books.add(book)
