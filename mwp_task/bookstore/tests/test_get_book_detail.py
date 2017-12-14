from .base_api_test import BookstoreBaseAPITestCase


class GetBooksDetailTestBase(BookstoreBaseAPITestCase):
    def test_get_books_by_anon(self):
        response = self.client.get('/books/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'id': 1, 'name': 'Clean code', 'photo': None,
            'description': 'How to write <i>code</i> well',
            'price': '0.01',
            'authors': [
                {'name': 'Robert', 'surname': 'Martin', 'photo': None},
            ]
        })

    def test_get_books_by_authorized(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.get('/books/2/')
        self.assertEqual(response.json(), {
            'id': 2, 'name': 'Code complete', 'photo': None,
            'description': 'How to write <i>code</i> well',
            'price': '0.02',
            'authors': [
                {'name': 'Steve', 'surname': 'McConnell', 'photo': None},
                {'name': 'Levi Metthew', 'surname': '', 'photo': None},
            ],
            'is_bought': True,
            'link': 'http://amazons3.com/books/code_complete.pdf',
        })

        response = self.client.get('/books/1/')
        self.assertEqual(response.json(), {
            'id': 1, 'name': 'Clean code', 'photo': None,
            'description': 'How to write <i>code</i> well',
            'price': '0.01',
            'authors': [
                {'name': 'Robert', 'surname': 'Martin', 'photo': None},
            ],
            'is_bought': False,
            'link': None,
        })

    def test_get_non_existing_book_detail(self):
        response = self.client.get('/books/100/')
        self.assertEqual(response.status_code, 404)
