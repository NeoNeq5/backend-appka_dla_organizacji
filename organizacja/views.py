from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Czlonek, WidokBazyCzlonkow, Czlonekkierunek
from .serializers import CzlonekSerializer, WidokBazyCzlonkowSerializer, CzlonekKierunekSerializer


# Wyświetlanie listy filtrowaniem i sortowaniem
class ListaCzlonkowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WidokBazyCzlonkow.objects.all()
    serializer_class = WidokBazyCzlonkowSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Wyszukiwanie po tych polach
    search_fields = ['czlonek_imie', 'czlonek_nazwisko', 'czlonek_email', 'indeks']

    # Sortowanie
    ordering_fields = ['czlonek_nazwisko', 'czlonek_imie', 'kierunek_nazwa', 'sekcja_nazwa']
    ordering = ['czlonek_nazwisko']                             # Domyślne sortowanie


# CRUD
class CzlonekCRUDViewSet(viewsets.ModelViewSet):
    queryset = Czlonek.objects.all()
    serializer_class = CzlonekSerializer


# Widok do przypisywania kierunków
class CzlonekKierunekViewSet(viewsets.ModelViewSet):
    queryset = Czlonekkierunek.objects.all()
    serializer_class = CzlonekKierunekSerializer