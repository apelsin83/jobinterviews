from django.contrib.auth import get_user_model, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from requests import HTTPError
from rest_framework import status, generics
from rest_framework.response import Response
from social.apps.django_app.utils import load_backend
from social.apps.django_app.utils import load_strategy
from social.exceptions import AuthAlreadyAssociated
from .permissions import IsAuthenticatedOrCreate
from .serializers import AuthSerializer

User = get_user_model()

GOOGLE_PROVIDER = 'google-oauth2'


class GoogleOAuth2Login(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    def create(self, request, *args, **kwargs):
        if 'backend' not in request.data:
            return Response({"errors": 'Specify backend type'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif request.data['backend'] != 'google':
            return Response({"errors": 'Wrong backend type'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            provider = GOOGLE_PROVIDER

        if 'access_token' not in request.data or not request.data['access_token']:
            return Response({"errors": 'Access_token is not provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        authed_user = request.user if not request.user.is_anonymous() else None
        strategy = load_strategy(request)
        backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        token = request.data['access_token']
        is_new = False
        try:
            user = backend.do_auth(token, user=authed_user)
            is_new = user.is_new
        except AuthAlreadyAssociated:
            return Response({"errors": "That social media account is already in use"},
                            status=status.HTTP_400_BAD_REQUEST)
        except HTTPError:
            try:
                user = User.objects.get(token=token)
                user.social_auth.get(provider=provider).refresh_token(strategy)
            except:
                return Response({"errors": "Unauthorized token for url"},
                                status=status.HTTP_403_FORBIDDEN)
        if user and user.is_active:
            auth_created = user.social_auth.get(provider=provider)
            if auth_created.access_token != user.token:
                user.token = auth_created.access_token
                user.save()
            resp = {'token': user.token,
                    'is_new': is_new,
                    'user_id': user.id}
            serializer = self.get_serializer(data=resp)
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            status_response = status.HTTP_201_CREATED if is_new else status.HTTP_200_OK
            return Response(serializer.data, status=status_response, headers=headers)
        else:
            return Response({"errors": "Error with social authentication"},
                            status=status.HTTP_400_BAD_REQUEST)


def main_page(request):
    user = request.user
    out = {user: request.user}
    if user.is_authenticated():
        auth_user = user.social_auth.get(provider=GOOGLE_PROVIDER)
        access_token = auth_user.extra_data.get('access_token', '')
        if user.token != access_token:
            user.token = access_token
            user.save()
        out = {'access_token': access_token,
               'refresh_token': auth_user.extra_data.get('refresh_token', ''),}
    return render(request, 'auth_api/main.html', out)


def logout_reguest(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))
