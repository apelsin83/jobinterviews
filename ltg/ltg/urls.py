from django.conf.urls import url, include
from auth_api import views


urlpatterns = [
    url(r'^$', views.main_page, name='main'),
    url(r'^logout$', views.logout_reguest, name='logout'),
    url(r'^api/v1/auth/$', views.GoogleOAuth2Login.as_view(), name="google_login"),
    url('', include('social.apps.django_app.urls', namespace='social'))
]
