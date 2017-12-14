from .base_api_test import BookstoreBaseAPITestCase


class GetTopBooksListTestBase(BookstoreBaseAPITestCase):
    def test_get_top_books(self):
        response = self.client.get('/books/top')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': 2, 'name': 'Code complete', 'photo': None,
             'authors': ['Steve McConnell', 'Levi Metthew']},
            {'id': 3, 'name': 'The art of software testing', 'photo': None,
             'authors': ['Glenford Myers', 'Levi Metthew']},
            {'id': 1, 'name': 'Clean code', 'photo': None,
             'authors': ['Robert Martin']},
        ])

    def test_get_top_book_cache(self):
        self.client.get('/books/top')
        self.assertNumQueries(0, self.client.get, '/books/top')
