from .base_api_test import BookstoreBaseAPITestCase


class GetBoughtBooksListTestBase(BookstoreBaseAPITestCase):
    def test_get_bought_books_by_authorized(self):
        self.client.login(username='achistyakov', password='password')
        response = self.client.get('/books/bought')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': 2, 'name': 'Code complete', 'photo': None,
             'authors': ['Steve McConnell', 'Levi Metthew'],
             'is_bought': True},
            {'id': 3, 'name': 'The art of software testing', 'photo': None,
             'authors': ['Glenford Myers', 'Levi Metthew'],
             'is_bought': True},
        ])

    def test_get_bought_books_by_anon(self):
        response = self.client.get('/books/bought')
        self.assertEqual(response.status_code, 403)
