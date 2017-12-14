from .base_api_test import BookstoreBaseAPITestCase


class GetBooksListTestBase(BookstoreBaseAPITestCase):
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
