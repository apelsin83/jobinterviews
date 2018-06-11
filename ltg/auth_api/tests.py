from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_api.views import GOOGLE_PROVIDER

User = get_user_model()


class AuthApiTests(APITestCase):
    fixtures = ['auth_api_data.json', 'social_data.json']

    def test_create_account(self):
        user = User.objects.all()[0]
        social_user = user.social_auth.get(provider=GOOGLE_PROVIDER)
        token = social_user.extra_data.get('access_token', '')

        # Renew token
        url = reverse('google_login')
        data = {'access_token': token,
                'backend': 'google'}
        response = self.client.post(url, data, format='json')
        token = response.data.get('token', '')
        data['access_token'] = token
        # clear fixture user
        user.delete()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_new'], True)
        self.assertEqual(response.data['token'], token)

    def test_exsisting_account(self):
        user = User.objects.all()[0]
        social_user = user.social_auth.get(provider=GOOGLE_PROVIDER)
        token = social_user.extra_data.get('access_token', '')
        url = reverse('google_login')
        data = {'access_token': token,
                'backend': 'google'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_new'], False)

    def test_post_without_token(self):
        url = reverse('google_login')
        data = {'backend': 'google'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], 'Access_token is not provided')

    def test_post_wrong_token(self):
        url = reverse('google_login')
        data = {'backend': 'google',
                'access_token': 'sdf'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.status_code == status.HTTP_200_OK)
        self.assertEqual(response.data['errors'], 'Unauthorized token for url')

    def test_empty_post(self):
        url = reverse('google_login')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], 'Specify backend type')

    def test_empty_backend(self):
        user = User.objects.all()[0]
        social_user = user.social_auth.get(provider=GOOGLE_PROVIDER)
        token = social_user.extra_data.get('access_token', '')
        url = reverse('google_login')
        response = self.client.post(url, {'access_token': token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], 'Specify backend type')

    def test_wrong_backend(self):
        user = User.objects.all()[0]
        social_user = user.social_auth.get(provider=GOOGLE_PROVIDER)
        token = social_user.extra_data.get('access_token', '')
        url = reverse('google_login')
        data = {'backend': 'googledfgdfg',
                'access_token': token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], 'Wrong backend type')

    def test_get(self):
        url = reverse('google_login')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
