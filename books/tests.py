import json

from .models     import Book, Author, AuthorBook, User
from django.test import TestCase, Client


class AuthorTest(TestCase):
    def setUp(self):
        Author.objects.create(
            name = '박세용',
            email = 'seyong0428@gmail.com'
        )

    def tearDown(self):
        Author.objects.all().delete()
    
    def test_authorview_post_success(self):
        client = Client()
        author = {
            'name' : '박개발',
            'email': 'parkdev@gmail.com'
        }
        response = client.post('/books/author', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    def test_authorview_post_duplicated_name(self):
        client = Client()
        author = {
            'name' : '박세용',
            'email': 'parkdev@gmail.com'
        }
        response = client.post('/books/author', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'DUPLICATED_NAME'})

    def test_authorview_post_invalid_keys(self):
        client = Client()
        author = {
            'first_name': '박개발',
            'email'     : 'parkdev@gmail.com'
        }
        response = client.post('/books/author', json.dumps(author), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_KEYS'})
    
    class AuthorBookTest(TestCase):
        def setUp(self):
            client = Client()
            Book.objects.create(
                id    = 1,
                title = 'python'
            )

            Book.objects.create(
                id    = 2,
                title = 'javascript'
            )

            Author.objects.create(
                id    = 1,
                name  = '박개발',
                email = 'parkdev@gmail.com'
            )
            
            Author.objects.create(
                id    = 2,
                name  = '박세용',
                email = 'sae0428@gmail.com'
            )

            AuthorBook.objects.create(
                book   = Book.objects.get(id=1),
                author = Author.objects.get(id=1)
            )

            AuthorBook.objects.create(
                book   = Book.objects.get(id=1),
                author = Author.objects.get(id=2)
            )

            AuthorBook.objects.create(
                book   = Book.objects.get(id=2),
                author = Author.objects.get(id=1)
            )

            AuthorBook.objects.create(
                book   = Book.objects.get(id=2),
                author = Author.objects.get(id=2)
            )

        def tearDown(self):
            Book.objects.all().delete()
            Author.objects.all().delete()
            AuthorBook.objects.all().delete()
        
        def test_authorbook_get_succes(self):
            client = Client()
            response = client.get('/books/author-book/1')
            self.assertEqual(response.json(),
                {
                    "authors" : [
                        {'author' : 1},
                        {'author' : 2}
                    ]
                }
            )
            self.assertEqual(response.status_code, 200)
