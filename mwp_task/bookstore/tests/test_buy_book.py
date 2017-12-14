import os
from unittest import mock

from .base_api_test import BookstoreBaseAPITestCase


class BuyBookTestBase(BookstoreBaseAPITestCase):
    def test_buy_book_status_code(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.post('/books/1/buy', data={'card_name': 'VISA***1111'})
        self.assertEqual(response.status_code, 200)

    def test_buy_book_sets_bought_status(self):
        self.client.login(username='achistyakov', password='password')
        self.client.post('/books/1/buy', data={'card_name': 'VISA***1111'})
        response = self.client.get('/books/1/')
        self.assertEqual(response.json()['is_bought'], True)

    def test_buy_book_by_anon(self):
        response = self.client.post('/books/1/buy', data={'card_name': 'foo'})
        self.assertEqual(response.status_code, 403)

    def test_buy_non_existing_book(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.post('/books/42/buy', data={'card_name': 'VISA***1111'})
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/books/1/')
        self.assertEqual(response.json()['is_bought'], False)

    def test_buy_already_bought_book(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.post('/books/2/buy', data={'card_name': 'VISA***1111'})
        self.assertEqual(response.status_code, 409)
        response = self.client.get('/books/2/')
        self.assertEqual(response.json()['is_bought'], True)

    def test_buy_book_by_alien_card(self):
        self.client.login(username='aapostle', password='password')
        response = self.client.post('/books/1/buy', data={'card_name': 'VISA***1111'})
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/books/1/')
        self.assertEqual(response.json()['is_bought'], False)

    def test_buy_book_by_non_existing_card(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.post('/books/1/buy', data={'card_name': 'VISA***2222'})
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/books/1/')
        self.assertEqual(response.json()['is_bought'], False)

    @mock.patch.dict(os.environ, {'PAYMENT_GETWAY_URL': 'http://www.mocky.io/v2/5a324f0f3100000c0b38b93f'})
    def test_payment_gateway_returns_failure(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.post('/books/1/buy', data={'card_name': 'VISA***1111'})
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/books/1/')
        self.assertEqual(response.json()['is_bought'], False)

    @mock.patch.dict(os.environ, {'PAYMENT_GETWAY_URL': 'http://fake/url'})
    def test_payment_getway_does_not_response(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.post('/books/1/buy', data={'card_name': 'VISA***1111'})
        self.assertEqual(response.status_code, 500)
        response = self.client.get('/books/1/')
        self.assertEqual(response.json()['is_bought'], False)

    @mock.patch.dict(os.environ, {'PAYMENT_GETWAY_URL': 'http://www.mocky.io/v2/5a32521e3100000b0b38b94b'})
    def test_payment_getway_response_with_invalid_json(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.post('/books/1/buy', data={'card_name': 'VISA***1111'})
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/books/1/')
        self.assertEqual(response.json()['is_bought'], False)
