from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view

from .models import Czlonek, WidokBazyCzlonkow, Czlonekkierunek, Czloneksekcji, Sekcja, Kierunek, Projekt, \
    Czlonekprojektu, WidokPartnerow, Partner, OdpowiedziSlownik, Przychod, Budzet, Wydatek
from .serializers import CzlonekSerializer, WidokBazyCzlonkowSerializer, CzlonekKierunekSerializer, \
    CzlonekSekcjiSerializer, SekcjaSerializer, KierunekSerializer, ProjektSerializer, CzlonekProjektuSerializer, \
    WidokPartnerowSerializer, PartnerSerializer, OdpowiedziSlownikSerializer, PrzychodSerializer, WydatekSerializer


# Słowniki
class OdpowiedziSlownikViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint zwracający opcje do dropdown dla statusy odpowiedzi partnerów"""
    queryset = OdpowiedziSlownik.objects.all().order_by('nazwa')
    serializer_class = OdpowiedziSlownikSerializer


# Moduł członków

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

    def perform_create(self, serializer):
        data = self.request.data

        with transaction.Atomic():
            czlonek = serializer.save()

            if 'kierunek' in data and data['kierunek']:
                Czlonekkierunek.objects.create(id_czlonek=czlonek, id_kierunku_id=data['kierunek'])
            if 'sekcja' in data and data['sekcja']:
                Czloneksekcji.objects.create(id_czlonek=czlonek, id_sekcja_id=data['sekcja'])
            if 'projekt' in data and data['projekt']:
                Czlonekprojektu.objects.create(id_czlonek=czlonek, id_projekt_id=data['projekt'])

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


# Moduł partnerów

@extend_schema_view(
    list=extend_schema(summary="Gotowy widok do modułu bazy partnerów", description="Wyświetla listę wszystkich partnerów wraz z pełnymi informacjami ze wszystkich tabel powiązanych."),
    retrieve=extend_schema(summary="Szczegóły danego partnera")
)
class ListaPartnerowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WidokPartnerow.objects.all()
    serializer_class = WidokPartnerowSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['partner_nazwa', 'osoba_odp_nazwisko']
    ordering_fields = ['partner_nazwa', 'przychod_kwota']


@extend_schema_view(
    list=extend_schema(summary="Lista danych tabeli partnerów"),
    create=extend_schema(summary="Dodaj partnera", description="Tworzy nowy wpis firmy partnerskiej."),
    retrieve=extend_schema(summary="Dane do formularza edycji"),
    update=extend_schema(summary="Pełna aktualizacja partnera"),
    partial_update=extend_schema(summary="Edytuj partnera", description="Pozwala na zmianę danych partnera (że ołówek)"),
    destroy=extend_schema(summary="Usuń partnera", description="Trwale usuwa firmę z bazy (że kosz)")
)
class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


@extend_schema_view(list=extend_schema(summary="Opcje odpowiedzi (Dropdown)"))
class OdpowiedziSlownikViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OdpowiedziSlownik.objects.all()
    serializer_class = OdpowiedziSlownikSerializer


# Moduł budżetu
@extend_schema_view(
    list=extend_schema(summary="Lista przychodów", description="Pobiera surowe dane z tabeli przychodów."),
    create=extend_schema(summary="Dodaj przychód", description="Tworzy rekord w tabeli Przychod i automatycznie wiąże go z tabelą Budzet."),
    destroy=extend_schema(summary="Usuń przychód", description="Usuwa przychód i powiązany wpis w tabeli Budzet.")
)
class PrzychodViewSet(viewsets.ModelViewSet):
    queryset = Przychod.objects.all()
    serializer_class = PrzychodSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            przychod = serializer.save()

            Budzet.objects.create(
                id_przychod=przychod,
                kwota=przychod.kwota,
                id_wydatek=None
            )


@extend_schema_view(
    list=extend_schema(summary="Lista wydatków", description="Pobiera dane z tabeli wydatków."),
    create=extend_schema(summary="Dodaj wydatek", description="Tworzy rekord w tabeli Wydatek i automatycznie wiąże go z tabelą Budzet."),
    destroy=extend_schema(summary="Usuń wydatek", description="Usuwa wydatek i powiązany wpis w tabeli Budzet.")
)
class WydatekViewSet(viewsets.ModelViewSet):
    queryset = Wydatek.objects.all()
    serializer_class = WydatekSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            wydatek = serializer.save()

            Budzet.objects.create(
                id_wydatek=wydatek,
                kwota=wydatek.kwota,
                id_przychod=None
            )


@extend_schema(summary="Pobierz aktualne saldo", description="Oblicza sumę przychodów minus sumę wydatków.")
@api_view(['GET'])
def pobierz_saldo(request):
    suma_przychodow = Przychod.objects.aggregate(total=Sum('kwota'))['total'] or 0
    suma_wydatkow = Wydatek.objects.aggregate(total=Sum('kwota'))['total'] or 0

    saldo = suma_przychodow - suma_wydatkow

    return Response({
        'saldo': saldo,
        'waluta': 'PLN',
        'suma_przychodow': suma_przychodow,
        'suma_wydatkow': suma_wydatkow
    })