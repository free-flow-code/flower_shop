"""flower_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from flower_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('catalog/', views.catalog_api, name='catalog'),
    path('catalog/<str:reason>/', views.catalog_sorted, name='catalog_sorted'),
    path('card/<int:id>/', views.card, name='card'),
    path('order/<int:id>/', views.order, name='order'),
    path('order_result/<int:id>/', views.order_result, name='order_result'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/<str:reason>/', views.quiz_step, name='quiz_step'),
    path('quiz_result/<str:reason>/<str:category>/', views.quiz_result, name='quiz_result'),
    path('manager/consults/', views.consultations, name='consultations'),
    path('consult/', views.create_consultation, name='create_consultation')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
