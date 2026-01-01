from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListaCzlonkowViewSet, CzlonekCRUDViewSet, CzlonekKierunekViewSet, SekcjaViewSet, KierunekViewSet, \
    CzlonekSekcjiViewSet, CzlonekProjektuViewSet, ProjektViewSet

router = DefaultRouter()

router.register(r'lista-czlonkow', ListaCzlonkowViewSet, basename='lista-czlonkow')
router.register(r'czlonkowie', CzlonekCRUDViewSet)

router.register(r'przypisz-kierunek', CzlonekKierunekViewSet)
router.register(r'kierunki', KierunekViewSet, basename='kierunki')

router.register(r'przypisz-sekcje', CzlonekSekcjiViewSet, basename='przypisz-sekcje')
router.register(r'sekcje', SekcjaViewSet, basename='sekcje')

router.register(r'przypisz-projekt', CzlonekProjektuViewSet, basename='przypisz-projekt')
router.register(r'projekty', ProjektViewSet, basename='projekty')

urlpatterns = [
    path('', include(router.urls)),
]