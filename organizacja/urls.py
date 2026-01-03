from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListaCzlonkowViewSet, CzlonekCRUDViewSet, CzlonekKierunekViewSet, SekcjaViewSet, KierunekViewSet, \
    CzlonekSekcjiViewSet, CzlonekProjektuViewSet, ProjektViewSet, PartnerViewSet, ListaPartnerowViewSet, \
    OdpowiedziSlownikViewSet, pobierz_saldo, PrzychodViewSet, WydatekViewSet

router = DefaultRouter()


#Słowniki
router.register(r'slownik-statusow', OdpowiedziSlownikViewSet, basename='slownik-statusow')


#Członkowie
router.register(r'lista-czlonkow', ListaCzlonkowViewSet, basename='lista-czlonkow')
router.register(r'czlonkowie', CzlonekCRUDViewSet)

router.register(r'przypisz-kierunek', CzlonekKierunekViewSet)
router.register(r'kierunki', KierunekViewSet, basename='kierunki')

router.register(r'przypisz-sekcje', CzlonekSekcjiViewSet, basename='przypisz-sekcje')
router.register(r'sekcje', SekcjaViewSet, basename='sekcje')

router.register(r'przypisz-projekt', CzlonekProjektuViewSet, basename='przypisz-projekt')
router.register(r'projekty', ProjektViewSet, basename='projekty')

#Partnerzy
router.register(r'partnerzy', PartnerViewSet, basename='partnerzy')
router.register(r'lista-partnerow', ListaPartnerowViewSet, basename='lista-partnerow')
router.register(r'partnerzy-statusy', OdpowiedziSlownikViewSet, basename='partnerzy-statusy')

#Budżet
router.register(r'przychody', PrzychodViewSet, basename='przychody')
router.register(r'wydatki', WydatekViewSet, basename='wydatki')

urlpatterns = [
    path('', include(router.urls)),
    path('budzet/saldo/', pobierz_saldo, name='pobierz-saldo'),
]