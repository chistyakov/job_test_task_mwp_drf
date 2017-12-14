from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Author, Book


class AuthorModelTest(TestCase):
    def test_string_representation(self):
        author = Author(name='Robert', surname='Martin')
        self.assertEqual(str(author), 'Robert Martin')


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alobachev', email='artem@mwptech.com', password='password',
        )
        self.user.save()
        self.user.profile.save()

    def test_profile_created_with_user(self):
        self.assertTrue(hasattr(self.user, 'profile'))

    def test_string_representation(self):
        self.assertEqual(str(self.user.profile), 'alobachev')

    def test_phone_field_has_validators(self):
        self.user.profile.phone = 'foo'
        self.assertRaises(ValidationError, self.user.profile.full_clean)

    def test_add_credit_card_to_profile(self):
        self.user.profile.cards.create(
            name='VISA***1111', payment_number='1111-1111-1111-1111'
        )
        cards = self.user.profile.cards.all()
        self.assertEqual(len(cards), 1)
        self.assertEqual(str(cards[0]), 'VISA***1111')

    def test_buy_book(self):
        book = Book(
            name='foo',
            description='bar',
            price=Decimal('0.00001'),
            link='http://example.com/book.pdf',
        )
        book.save()
        self.user.profile.bought_books.add(book)
        self.assertEqual(list(book.buyers.all()), [self.user.profile])


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book(
            name='Clean code',
            description='How to write <i>code</i> well',
            price=Decimal('0.01'),
            link='http://amazons3.com/rmartin/clean_code.pdf',
        )
        self.book.save()

    def test_string_representation(self):
        self.assertEqual(str(self.book), 'Clean code')

    def test_add_few_books_authors(self):
        uncle_bob = Author(name='Robert', surname='Marting')
        uncle_bob.save()
        self.book.authors.add(uncle_bob)
        levi_metthew = self.book.authors.create(name='Levi Matthew')
        self.assertEqual(list(levi_metthew.books.all()), [self.book])
