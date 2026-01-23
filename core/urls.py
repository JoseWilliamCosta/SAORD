from django.urls import path
from .views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # parte basica de autenticação
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('logout/', logout_view, name='logout'),
    path("perfil/", perfil_usuario, name="perfil"),
    path("perfil/atualizar/", atualizar_usuario, name="atualizar_usuario"),
    path("perfil/excluir/", excluir_usuario, name="excluir_usuario"),




    #logica de sessões e documentos
    path('session/create/', create_session, name='create_session'),
    path('session/<int:session_id>/edit/', edit_session, name='edit_session'),
    path('session/<int:session_id>/delete/', delete_session, name='delete_session'),
    path('session/<int:session_id>/', session_detail, name='session_detail'),

    path('session/<int:session_id>/document/create/', create_document, name='create_document'),
    path('document/<int:document_id>/edit/', edit_document, name='edit_document'),
    path('document/<int:document_id>/delete/', delete_document, name='delete_document'),


    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )