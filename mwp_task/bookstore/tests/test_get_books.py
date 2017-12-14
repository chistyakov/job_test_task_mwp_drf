from decimal import Decimal

from bookstore.models import Book, Author
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class GetBooksListTest(APITestCase):
    def setUp(self):
        uncle_bob = Author(name='Robert', surname='Martin')
        uncle_bob.save()
        mcconnell = Author(name='Steve', surname='McConnell')
        mcconnell.save()
        myers = Author(name='Glenford', surname='Myers')
        myers.save()
        levi_metthew = Author(name='Levi Metthew')
        levi_metthew.save()

        clean_code = Book(
            name='Clean code',
            description='How to write <i>code</i> well',
            price=Decimal('0.01'),
            link='http://amazons3.com/books/clean_code.pdf',
        )
        clean_code.save()
        clean_code.authors.add(uncle_bob)

        code_complete = Book(
            name='Code complete',
            description='How to write <i>code</i> well',
            price=Decimal('0.02'),
            link='http://amazons3.com/books/code_complete.pdf',
        )
        code_complete.save()
        code_complete.authors.add(mcconnell)
        code_complete.authors.add(levi_metthew)

        the_art_of_software_testing = Book(
            name='The art of software testing',
            description='The first book about software testing',
            price=Decimal('0.003'),
            link='http://amazons3.com/books/the_art_of_software_testing.pdf'
        )
        the_art_of_software_testing.save()
        the_art_of_software_testing.authors.add(myers)
        the_art_of_software_testing.authors.add(levi_metthew)

        alobachev = User(username='alobachev', email='artem@mwptech.com')
        alobachev.set_password('password')
        alobachev.save()
        alobachev.profile.bought_books.add(code_complete)
        achistyakov = User(username='achistyakov', email='al.ol.chistyakov@gmail.com')
        achistyakov.set_password('password')
        achistyakov.save()
        achistyakov.profile.bought_books.add(code_complete, the_art_of_software_testing)
        aukupnik = User(username='aukupnik', email='arkady@ukupnik.io')
        aukupnik.set_password('password')
        aukupnik.save()
        aukupnik.profile.bought_books.add(code_complete, the_art_of_software_testing, clean_code)
        aapostle = User(username='aapostle', email='Andrew@apostle.xxx')
        aapostle.set_password('password')
        aapostle.save()

    def test_get_books_by_anon(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': 1, 'name': 'Clean code', 'photo': None,
             'authors': ['Robert Martin']},
            {'id': 2, 'name': 'Code complete', 'photo': None,
             'authors': ['Steve McConnell', 'Levi Metthew']},
            {'id': 3, 'name': 'The art of software testing', 'photo': None,
             'authors': ['Glenford Myers', 'Levi Metthew']},
        ])

    def test_get_books_by_authorized(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': 1, 'name': 'Clean code', 'photo': None,
             'authors': ['Robert Martin'],
             'is_bought': False},
            {'id': 2, 'name': 'Code complete', 'photo': None,
             'authors': ['Steve McConnell', 'Levi Metthew'],
             'is_bought': True},
            {'id': 3, 'name': 'The art of software testing', 'photo': None,
             'authors': ['Glenford Myers', 'Levi Metthew'],
             'is_bought': True},
        ])

    def test_get_books_filers(self):
        response = self.client.get('/books/?name=Clean+code')
        self.assertEqual(response.json(), [
            {'id': 1, 'name': 'Clean code', 'photo': None,
             'authors': ['Robert Martin']},
        ])
        response = self.client.get('/books/?authors__name=Levi+Metthew')
        self.assertEqual(response.json(), [
            {'id': 2, 'name': 'Code complete', 'photo': None,
             'authors': ['Steve McConnell', 'Levi Metthew']},
            {'id': 3, 'name': 'The art of software testing', 'photo': None,
             'authors': ['Glenford Myers', 'Levi Metthew']},
        ])

    def test_get_books_searches(self):
        response = self.client.get('/books/?search=code')
        self.assertEqual(response.json(), [
            {'id': 1, 'name': 'Clean code', 'photo': None,
             'authors': ['Robert Martin']},
            {'id': 2, 'name': 'Code complete', 'photo': None,
             'authors': ['Steve McConnell', 'Levi Metthew']},
        ])

    def tearDown(self):
        self.client.logout()
