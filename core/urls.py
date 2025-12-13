from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    
    # === api ===
    #path('api/notas/', notas_filtradas_api, name='notas_filtradas_api'),
    
]
