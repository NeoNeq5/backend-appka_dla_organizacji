from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListaCzlonkowViewSet, CzlonekCRUDViewSet, CzlonekKierunekViewSet

router = DefaultRouter()
router.register(r'lista-czlonkow', ListaCzlonkowViewSet, basename='lista-czlonkow')
router.register(r'czlonkowie', CzlonekCRUDViewSet)
router.register(r'przypisz-kierunek', CzlonekKierunekViewSet)

urlpatterns = [
    path('', include(router.urls)),
]