from json import dumps
import datetime

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .models import ActivityReport


class UserLoginTest(APITestCase):

    def setUp(self):
        data_user = {
            'username': 'jhon', 'email': 'jhon@example.com',
            'first_name': 'Jhon', 'last_name': 'Doe', 'password': '12345678as'
        }
        User.objects.create_user(**data_user)

    def test_login_ok(self):
        data = {'username': 'jhon', 'password': '12345678as'}

        response = self.client.post(
            '/user/login/', dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(True, 'user' in response.json().keys())
        self.assertEqual(True, 'access_token' in response.json().keys())

    def test_login_invalid_password(self):
        data = {'username': 'jhon', 'password': '12345678at'}

        response = self.client.post(
            '/user/login/', dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        keys = response.json().keys()
        self.assertEqual(True, 'non_field_errors' in keys)
        self.assertEqual(
            ['Invalid credentials.'],
            response.json().get('non_field_errors'))

    def test_login_password_len(self):
        data = {'username': 'jhon', 'password': '12345'}

        response = self.client.post(
            '/user/login/', dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(True, 'password' in response.json().keys())
        self.assertEqual(
            ['Ensure this field has at least 8 characters.'],
            response.json().get('password'))


class UserCreateTest(APITestCase):

    def test_create_ok(self):
        data = {
            'username': 'jhon', 'email': 'jhon@example.com',
            'first_name': 'Jhon', 'last_name': 'Doe',
            'password': '12345678as', 'password_confirmation': '12345678as'
        }

        response = self.client.post(
            '/user/', dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        keys = response.json().keys()
        self.assertEqual(True, 'id' in keys)
        self.assertEqual(True, 'username' in keys)
        self.assertEqual(True, 'email' in keys)
        self.assertEqual(True, 'first_name' in keys)
        self.assertEqual(True, 'last_name' in keys)
        self.assertEqual(False, 'password' in keys)
        self.assertEqual(False, 'password_confirmation' in keys)

    def test_create_blank(self):
        data = {}
        response = self.client.post(
            '/user/', dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertListEqual(
            [
                'email', 'username', 'password', 'password_confirmation',
                'first_name', 'last_name'
            ],
            list(response.json().keys())
        )
        self.assertEqual(
            ['This field is required.'],
            response.json().get('email'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('username'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('password'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('password_confirmation'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('first_name'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('last_name'))


class UserUpdateTest(APITestCase):

    def setUp(self):
        data_user1 = {
            'username': 'jhon', 'email': 'jhon@example.com',
            'first_name': 'Jhon', 'last_name': 'Doe', 'password': '12345678as'
        }
        self.user = User.objects.create_user(**data_user1)
        Token.objects.get_or_create(user=self.user)
        data_user2 = {
            'username': 'jhon1', 'email': 'jhon1@example.com',
            'first_name': 'Jhon1', 'last_name': 'Doe1',
            'password': '12345678as'
        }
        self.user2 = User.objects.create_user(**data_user2)

    def test_update_ok(self):
        data = {
            'username': 'jhon2', 'email': 'jhon2@example.com',
            'first_name': 'Jhon2', 'last_name': 'Doe2',
            'password': '12345678as1', 'password_confirmation': '12345678as1'
        }

        client = APIClient(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = client.put(
            '/user/%s/' % self.user2.id, dumps(data),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()), 5)
        self.assertEqual(self.user2.id, response.json().get('id'))
        self.assertEqual('jhon2', response.json().get('username'))
        self.assertEqual('jhon2@example.com', response.json().get('email'))
        self.assertEqual('Jhon2', response.json().get('first_name'))
        self.assertEqual('Doe2', response.json().get('last_name'))

    def test_update_blank(self):
        data = {}
        client = APIClient(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = client.put(
            '/user/%s/' % self.user2.id, dumps(data),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertListEqual(
            [
                'email', 'username', 'password', 'password_confirmation',
                'first_name', 'last_name'
            ],
            list(response.json().keys())
        )
        self.assertEqual(
            ['This field is required.'],
            response.json().get('email'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('username'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('password'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('password_confirmation'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('first_name'))
        self.assertEqual(
            ['This field is required.'],
            response.json().get('last_name'))

    def test_update_no_token(self):
        client = APIClient()
        data = {
            'username': 'jhon2', 'email': 'jhon2@example.com',
            'first_name': 'Jhon2', 'last_name': 'Doe2',
            'password': '12345678as1', 'password_confirmation': '12345678as1'
        }
        response = client.put(
            '/user/%s/' % self.user2.id, dumps(data),
            content_type='application/json')

        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Authentication credentials were not provided.',
            response.json().get('detail'))

    def test_update_invalid_token(self):
        data = {
            'username': 'jhon2', 'email': 'jhon2@example.com',
            'first_name': 'Jhon2', 'last_name': 'Doe2',
            'password': '12345678as1', 'password_confirmation': '12345678as1'
        }
        client = APIClient(
            HTTP_AUTHORIZATION='Token 1212212212')
        response = client.put(
            '/user/%s/' % self.user2.id, dumps(data),
            content_type='application/json')

        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Invalid token.',
            response.json().get('detail'))


class UserListTest(APITestCase):

    def setUp(self):
        data_user1 = {
            'username': 'jhon', 'email': 'jhon@example.com',
            'first_name': 'Jhon', 'last_name': 'Doe', 'password': '12345678as'
        }
        self.user = User.objects.create_user(**data_user1)
        Token.objects.get_or_create(user=self.user)
        data_user2 = {
            'username': 'jhon1', 'email': 'jhon1@example.com',
            'first_name': 'Jhon1', 'last_name': 'Doe1',
            'password': '12345678as'
        }
        User.objects.create_user(**data_user2)

    def test_list_ok(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = client.get('/user/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.json()), 2)

    def test_list_no_token(self):
        client = APIClient()
        response = client.get('/user/')
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Authentication credentials were not provided.',
            response.json().get('detail'))

    def test_list_invalid_token(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token 1212212212')
        response = client.get('/user/')
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Invalid token.',
            response.json().get('detail'))


class UserRetrieveTest(APITestCase):

    def setUp(self):
        data_user = {
            'username': 'jhon', 'email': 'jhon@example.com',
            'first_name': 'Jhon', 'last_name': 'Doe', 'password': '12345678as'
        }
        self.user = User.objects.create_user(**data_user)
        Token.objects.get_or_create(user=self.user)

    def test_retrieve_ok(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = client.get('/user/%s/' % self.user.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.json()), 5)
        self.assertEqual(self.user.id, response.json().get('id'))
        self.assertEqual(self.user.username, response.json().get('username'))
        self.assertEqual(self.user.email, response.json().get('email'))
        self.assertEqual(
            self.user.first_name, response.json().get('first_name'))
        self.assertEqual(self.user.last_name, response.json().get('last_name'))

    def test_retrieve_invalid_id(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = client.get('/user/%s/' % self.user.id * 1024)
        self.assertEqual(404, response.status_code)

    def test_retrieve_no_token(self):
        client = APIClient()
        response = client.get('/user/%s/' % self.user.id)
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Authentication credentials were not provided.',
            response.json().get('detail'))

    def test_retrieve_invalid_token(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token 1212212212')
        response = client.get('/user/%s/' % self.user.id)
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Invalid token.',
            response.json().get('detail'))


class UserDeleteTest(APITestCase):

    def setUp(self):
        data_user1 = {
            'username': 'jhon', 'email': 'jhon@example.com',
            'first_name': 'Jhon', 'last_name': 'Doe', 'password': '12345678as'
        }
        self.user = User.objects.create_user(**data_user1)
        Token.objects.get_or_create(user=self.user)
        data_user2 = {
            'username': 'jhon1', 'email': 'jhon1@example.com',
            'first_name': 'Jhon1', 'last_name': 'Doe1',
            'password': '12345678as'
        }
        self.user2 = User.objects.create_user(**data_user2)

    def test_delete_ok(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = client.delete('/user/%s/' % self.user2.id)
        self.assertEqual(204, response.status_code)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_invalid_id(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = client.delete('/user/%s/' % self.user2.id * 1024)
        self.assertEqual(404, response.status_code)
        self.assertEqual(User.objects.count(), 2)

    def test_delete_no_token(self):
        client = APIClient()
        response = client.delete('/user/%s/' % self.user2.id)
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Authentication credentials were not provided.',
            response.json().get('detail'))

    def test_delete_invalid_token(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token 1212212212')
        response = client.get('/user/%s/' % self.user2.id)
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Invalid token.',
            response.json().get('detail'))


class ActivityReportTest(APITestCase):

    def setUp(self):
        self.data_user1 = {
            'username': 'jhon', 'email': 'jhon@example.com',
            'first_name': 'Jhon', 'last_name': 'Doe', 'password': '12345678as'
        }
        self.user1 = User.objects.create_user(**self.data_user1)
        Token.objects.get_or_create(user=self.user1)
        self.data_user2 = {
            'username': 'jhon1', 'email': 'jhon1@example.com',
            'first_name': 'Jhon1', 'last_name': 'Doe1',
            'password': '12345678as'
        }
        self.user2 = User.objects.create_user(**self.data_user2)

        for i in range(3):
            a1 = ActivityReport.objects.create(user=self.user1)
            a1.date = datetime.date(2020, 12, 18)
            a2 = ActivityReport.objects.create(user=self.user2)
            a2.date = datetime.date(2020, 12, 18)
            a1.save()
            a2.save()

        a3 = ActivityReport.objects.create(user=self.user2)
        a3.date = datetime.date(2020, 11, 18)
        a3.save()

    def test_report_day_ok(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key)
        response = client.get('/activityReport/day/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.json()), 3)
        self.assertListEqual(
            [
                {'user': 'jhon1', 'date': '18/11/2020', 'count': 1},
                {'user': 'jhon', 'date': '18/12/2020', 'count': 3},
                {'user': 'jhon1', 'date': '18/12/2020', 'count': 3}
            ],
            response.json()
        )

    def test_report_day_no_token(self):
        client = APIClient()
        response = client.get('/activityReport/day/')
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Authentication credentials were not provided.',
            response.json().get('detail'))

    def test_report_day_invalid_token(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token 1212212212')
        response = client.get('/activityReport/day/')
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Invalid token.',
            response.json().get('detail'))

    def test_report_month_ok(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token ' + self.user1.auth_token.key)
        response = client.get('/activityReport/month/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.json()), 3)
        self.assertListEqual(
            [
                {'user': 'jhon1', 'date': '11/2020', 'count': 1},
                {'user': 'jhon', 'date': '12/2020', 'count': 3},
                {'user': 'jhon1', 'date': '12/2020', 'count': 3}
            ],
            response.json()
        )

    def test_report_month_no_token(self):
        client = APIClient()
        response = client.get('/activityReport/month/')
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Authentication credentials were not provided.',
            response.json().get('detail'))

    def test_report_month_invalid_token(self):
        client = APIClient(
            HTTP_AUTHORIZATION='Token 1212212212')
        response = client.get('/activityReport/month/')
        self.assertEqual(401, response.status_code)
        self.assertEqual(True, 'detail' in response.json().keys())
        self.assertEqual(
            'Invalid token.',
            response.json().get('detail'))
