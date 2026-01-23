from rest_framework.routers import DefaultRouter
from .views_api import SessionViewSet, DocumentViewSet

router = DefaultRouter()
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = router.urls