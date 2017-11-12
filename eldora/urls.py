from django.conf.urls import url
from django.contrib import admin
from telegram_backend import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^setUserId/', views.set_user_id, name='setUser'),
    url(r'^getUser/', views.get_user, name='getUser'),
    url(r'^setUserState/', views.set_user_state, name='setUserState'),
    url(r'^setUserStart/', views.set_user_start, name='setUserStart'),
    url(r'^setUserRate/', views.set_user_rate, name='setUserRate'),
    url(r'^setPhoneState/', views.set_phone_state, name='setPhoneState'),
    url(r'^setPhoneNumber/', views.set_phone_number, name='setPhoneNumber'),
]
