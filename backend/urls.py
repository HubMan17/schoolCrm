"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from crm import views

crm_api_urlpatterns = [
    path('', views.api_crm, name='api_crm'),
    path('get_stages', views.api_crm_get_stages, name='api_crm_get_stages'),
    path('get_cards', views.api_crm_get_cards, name='api_crm_get_cards'),
    path('update_stage_card', views.api_crm_update_idStage_card, name='api_crm_update_stage_card'),
    path('get_specialties', views.api_crm_get_specialties, name='api_crm_get_specialties'),
    path('fast_create_card', views.api_crm_create_fast_card, name='api_crm_fast_create_card'),
]

urlpatterns = [
    path('', views.index, name='home'),
    path('api/', include(crm_api_urlpatterns)),
]
