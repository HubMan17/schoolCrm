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
from django.conf.urls.static import static
from django.conf import settings

from crm import views

crm_api_urlpatterns = [
    path('', views.api_crm, name='api_crm'),
    path('get_stages', views.api_crm_get_stages, name='api_crm_get_stages'),
    path('get_cards', views.api_crm_get_cards, name='api_crm_get_cards'),
    path('update_stage_card', views.api_crm_update_idStage_card, name='api_crm_update_stage_card'),
    path('get_specialties', views.api_crm_get_specialties, name='api_crm_get_specialties'),
    path('fast_create_card', views.api_crm_create_fast_card, name='api_crm_fast_create_card'),
    path('delete_card', views.api_crm_delete_card, name='api_crm_delete_card'),
    path('update_stage', views.api_crm_update_stage, name='api_crm_update_stage'),
    path('get_data_for_form', views.api_crm_get_data_for_form, name='get_data_for_form'),
    path('create_full_form', views.api_crm_create_card_from_full_form, name='create_card_from_full_form'),
    path('update_full_form', views.api_crm_update_card_from_full_form, name='update_card_from_full_form'),
    path('create_comment', views.api_crm_create_comment, name='api_crm_create_comment'),
    path('delete_comment', views.api_crm_delete_comment, name='api_crm_delete_comment'),
    path('update_comment', views.api_crm_update_comment, name='api_crm_update_comment'),
    
    path('crm_authorization', views.api_crm_authorization, name='api_crm_authorization'),
    path('crm_check_token', views.api_crm_get_token, name='api_crm_get_token'),
    # path('update_comment', views.api_crm_update_comment, name='api_crm_update_comment'),
    
    path('crm_get_users', views.api_crm_get_users, name='api_crm_get_users'),
    path('crm_update_users', views.api_crm_update_users, name='api_crm_update_users'),

    path('get_file', views.api_crm_get_file, name='api_crm_get_file'),

    path('test', views.test, name='test'),
]

urlpatterns = [
    path('', views.index, name='home'),
    path('api/', include(crm_api_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

