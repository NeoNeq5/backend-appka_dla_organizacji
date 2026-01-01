from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Czlonek, WidokBazyCzlonkow, Czlonekkierunek, Czloneksekcji, Sekcja, Kierunek, Projekt, \
    Czlonekprojektu
from .serializers import CzlonekSerializer, WidokBazyCzlonkowSerializer, CzlonekKierunekSerializer, \
    CzlonekSekcjiSerializer, SekcjaSerializer, KierunekSerializer, ProjektSerializer, CzlonekProjektuSerializer


@extend_schema_view(
    list=extend_schema(summary="Gotowy widok do modułu bazy członków", description="Wyświetla listę wszystkich członków wraz z pełnymi informacjami ze wszystkich tabel powiązanych."),
    retrieve=extend_schema(summary="Szczegóły danego członka", description="Wyświetla dane konkretnego członka po jego ID."),
)
class ListaCzlonkowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WidokBazyCzlonkow.objects.all()
    serializer_class = WidokBazyCzlonkowSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Wyszukiwanie po tych polach
    search_fields = ['czlonek_imie', 'czlonek_nazwisko', 'czlonek_email', 'indeks']

    # Sortowanie
    ordering_fields = ['czlonek_nazwisko', 'czlonek_imie', 'kierunek_nazwa', 'sekcja_nazwa']
    ordering = ['czlonek_nazwisko']                             # Domyślne sortowanie


@extend_schema_view(
    list=extend_schema(summary="Lista danych tabeli członek", description="Pobiera listę rekordów bezpośrednio z tabeli Czlonek."),
    create=extend_schema(summary="Dodaj nowego członka do tabeli członek", description="Tworzy nowy rekord członka. Wymaga podstawowych danych (imię, nazwisko, email)."),
    retrieve=extend_schema(summary="Szczegóły członka w tabeli członek", description="Pobiera surowe dane profilowe członka."),
    update=extend_schema(summary="Pełna edycja danych członka w tabeli członek", description="Nadpisuje wszystkie pola w tabeli Czlonek."),
    partial_update=extend_schema(summary="Szybka edycja danych członka w tabli członek", description="Pozwala na zmianę wybranych pól, np. tylko numeru telefonu."),
    destroy=extend_schema(summary="Usuń wiersz z tabeli członek", description="Usuwa rekord członka. Trigery w bazie SQL automatycznie wyczyszczą jego relacje.")
)
class CzlonekCRUDViewSet(viewsets.ModelViewSet):
    queryset = Czlonek.objects.all()
    serializer_class = CzlonekSerializer


@extend_schema_view(
    list=extend_schema(summary="Lista kierunków do dropdown", description="Pobiera listę kierunków studiów dostępnych w organizacji."),
    create=extend_schema(summary="Dodaj nowy kierunek"),
    retrieve=extend_schema(summary="Szczegóły kierunku",
                           description="Pobiera nazwę i opis konkretnego kierunku po ID."),
    update=extend_schema(summary="Pełna edycja kierunku"),
    partial_update=extend_schema(summary="Szybka edycja kierunku"),
    destroy=extend_schema(summary="Usuń kierunek")
)
class KierunekViewSet(viewsets.ModelViewSet):
    queryset = Kierunek.objects.all()
    serializer_class = KierunekSerializer


@extend_schema_view(
    list=extend_schema(summary="Lista sekcji do dropdown", description="Pobiera listę sekcji działających w organizacji (np. IT, Marketing)."),
    create=extend_schema(summary="Dodaj nową sekcję"),
    retrieve=extend_schema(summary="Szczegóły sekcji"),
    update=extend_schema(summary="Pełna edycja sekcji"),
    partial_update=extend_schema(summary="Szybka edycja sekcji"),
    destroy=extend_schema(summary="Usuń sekcję")
)
class SekcjaViewSet(viewsets.ModelViewSet):
    queryset = Sekcja.objects.all()
    serializer_class = SekcjaSerializer


@extend_schema_view(
    list=extend_schema(summary="Lista projektów do dropdown", description="Pobiera listę wszystkich projektów realizowanych przez organizację."),
    create=extend_schema(summary="Dodaj nowy projekt"),
    retrieve=extend_schema(summary="Szczegóły projektu", description="Pobiera dane konkretnego projektu po ID."),
    update=extend_schema(summary="Pełna edycja projektu"),
    partial_update=extend_schema(summary="Szybka edycja projektu"),
    destroy=extend_schema(summary="Usuń projekt")
)
class ProjektViewSet(viewsets.ModelViewSet):
    queryset = Projekt.objects.all()
    serializer_class = ProjektSerializer


@extend_schema_view(
    list=extend_schema(summary="Lista wszystkich przypisań do kierunków",
                       description="Pobiera listę ID członków i przypisanych im ID kierunków."),
    create=extend_schema(summary="Przypisz członka do kierunku",
                         description="Tworzy relację między członkiem a kierunkiem studiów."),
    retrieve=extend_schema(summary="Szczegóły przypisania kierunku",
                           description="Pobiera konkretne powiązanie członka z kierunkiem."),
    update=extend_schema(summary="Pełna edycja przypisania kierunku"),
    partial_update=extend_schema(summary="Szybka edycja przypisania kierunku"),
    destroy=extend_schema(summary="Usuń przypisanie do kierunku",
                          description="Usuwa powiązanie. Członek i kierunek pozostają w bazie, znika tylko ich relacja.")
)
class CzlonekKierunekViewSet(viewsets.ModelViewSet):
    queryset = Czlonekkierunek.objects.all()
    serializer_class = CzlonekKierunekSerializer


@extend_schema_view(
    list=extend_schema(summary="Lista wszystkich przypisań do sekcji",
                       description="Pobiera listę członków wraz z sekcjami, do których należą."),
    create=extend_schema(summary="Przypisz członka do sekcji",
                         description="Dodaje członka do wybranej sekcji (np. IT, Marketing)."),
    retrieve=extend_schema(summary="Szczegóły przypisania do sekcji"),
    update=extend_schema(summary="Pełna edycja przypisania do sekcji"),
    partial_update=extend_schema(summary="Szybka edycja przypisania do sekcji"),
    destroy=extend_schema(summary="Usuń członka z sekcji")
)
class CzlonekSekcjiViewSet(viewsets.ModelViewSet):
    queryset = Czloneksekcji.objects.all()
    serializer_class = CzlonekSekcjiSerializer


@extend_schema_view(
list=extend_schema(summary="Lista wszystkich przypisań do projektów", description="Pobiera listę pokazującą, kto bierze udział w jakich projektach."),
    create=extend_schema(summary="Przypisz członka do projektu", description="Dodaje członka jako uczestnika konkretnego projektu."),
    retrieve=extend_schema(summary="Szczegóły przypisania do projektu"),
    update=extend_schema(summary="Pełna edycja przypisania do projektu"),
    partial_update=extend_schema(summary="Szybka edycja przypisania do projektu"),
    destroy=extend_schema(summary="Usuń członka z projektu")
)
class CzlonekProjektuViewSet(viewsets.ModelViewSet):
    queryset = Czlonekprojektu.objects.all()
    serializer_class = CzlonekProjektuSerializer