from django.conf.urls import url
from django.contrib import admin
from telegram_backend import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^setUserID/', views.set_user_id, name='setUserId'),
    url(r'^setUserRate/', views.set_user_rate, name='set_user_rate'),
    url(r'^checkStart/', views.check_start, name='checkStart'),
]
