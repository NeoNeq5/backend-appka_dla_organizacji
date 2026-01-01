from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Czlonek, WidokBazyCzlonkow, Czlonekkierunek, Czloneksekcji, Sekcja, Kierunek, Projekt, \
    Czlonekprojektu
from .serializers import CzlonekSerializer, WidokBazyCzlonkowSerializer, CzlonekKierunekSerializer, \
    CzlonekSekcjiSerializer, SekcjaSerializer, KierunekSerializer, ProjektSerializer, CzlonekProjektuSerializer


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


# Przypisywanie kierunków
class CzlonekKierunekViewSet(viewsets.ModelViewSet):
    queryset = Czlonekkierunek.objects.all()
    serializer_class = CzlonekKierunekSerializer


class KierunekViewSet(viewsets.ModelViewSet):
    queryset = Kierunek.objects.all()
    serializer_class = KierunekSerializer


# Przypisywanie sekcji
class SekcjaViewSet(viewsets.ModelViewSet):
    queryset = Sekcja.objects.all()
    serializer_class = SekcjaSerializer


class CzlonekSekcjiViewSet(viewsets.ModelViewSet):
    queryset = Czloneksekcji.objects.all()
    serializer_class = CzlonekSekcjiSerializer


# Przypisywanie projektów
class ProjektViewSet(viewsets.ModelViewSet):
    queryset = Projekt.objects.all()
    serializer_class = ProjektSerializer


class CzlonekProjektuViewSet(viewsets.ModelViewSet):
    queryset = Czlonekprojektu.objects.all()
    serializer_class = CzlonekProjektuSerializer
