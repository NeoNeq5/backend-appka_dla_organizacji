from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Czlonek, Przychod, Wydatek, Partner, OdpowiedziSlownik


class CzlonekAPITests(APITestCase):
    def setUp(self):
        self.url = '/api/czlonkowie/'

    def test_dodaj_czlonka_sukces(self):
        data = {
            "imie": "Jan",
            "nazwisko": "Kowalski",
            "e_mail": "jan.kowalski@test.pl",
            "indeks": 112233,
            "telefon": 123456789
        }
        response = self.client.post(self.url, data, format='json')

        # 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # czy  jest 1 rekord
        self.assertEqual(Czlonek.objects.count(), 1)
        # czy imię się zgadza
        self.assertEqual(Czlonek.objects.get().imie, "Jan")


    def test_unikalnosc_indeksu(self):
        Czlonek.objects.create(
            imie="Pierwszy", nazwisko="Test", e_mail="1@test.pl", indeks=100100
        )

        data = {
            "imie": "Drugi",
            "nazwisko": "Zly",
            "e_mail": "2@test.pl",
            "indeks": 100100
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_brak_wymaganych_pol(self):
        data = {
            "e_mail": "tylko_email@test.pl"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('imie', response.data)
        self.assertIn('nazwisko', response.data)

    def test_limit_znakow_imie(self):
        bardzo_dlugie_imie = "A" * 51
        data = {
            "imie": bardzo_dlugie_imie,
            "nazwisko": "Test",
            "e_mail": "dlugi@test.pl"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BudzetAPITests(APITestCase):
    def setUp(self):
        self.osoba = Czlonek.objects.create(
            imie="Skarbnik",
            nazwisko="Testowy",
            e_mail="skarbnik@organizacja.pl"
        )
        self.url_przychod = '/api/przychody/'
        self.url_wydatek = '/api/wydatki/'
        self.url_saldo = '/api/saldo/'


    def test_obliczanie_salda(self):
        try:
            self.url_saldo = reverse('pobierz-saldo')
        except:
            self.url_saldo = '/api/saldo/'

        # przychód 100 zł
        Przychod.objects.create(
            kwota=100.00, nazwa="Grant", data=timezone.now(), osoba_odpowiedzialna=self.osoba
        )
        # wydatek 30 zł
        Wydatek.objects.create(
            kwota=30.00, nazwa="Druk", data=timezone.now(), osoba_odpowiedzialna=self.osoba
        )

        response = self.client.get(self.url_saldo)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Oczekiwane saldo: 100 - 30 = 70
        self.assertEqual(float(response.data['saldo']), 70.00)
        self.assertEqual(float(response.data['suma_przychodow']), 100.00)
        self.assertEqual(float(response.data['suma_wydatkow']), 30.00)

    def test_wydatek_bez_osoby_odpowiedzialnej(self):
        data = {
            "kwota": "10.00",
            "nazwa": "Błąd",
            "data": timezone.now().isoformat()
            # Brak osoba_odpowiedzialna
        }
        response = self.client.post(self.url_wydatek, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PartnerAPITests(APITestCase):
    def setUp(self):
        # członka, który będzie osobą odpowiedzialną
        self.czlonek = Czlonek.objects.create(
            imie="Anna",
            nazwisko="Nowak",
            e_mail="a.nowak@org.pl"
        )

        # wpis w słowniku odpowiedzi
        self.status_odp = OdpowiedziSlownik.objects.create(
            nazwa="Zainteresowany",
            opis="Partner wyraził chęć współpracy"
        )

        try:
            self.url_partnerzy = reverse('lista-partnerow')
        except:
            self.url_partnerzy = '/api/partnerzy/'

    def test_dodaj_partnera_sukces(self):
        data = {
            "nazwa": "Tech Solutions Sp. z o.o.",
            "numer_telefonu": 555666777,
            "e_mail": "biuro@techsolutions.pl",
            "osoba_odpowiedzialna": self.czlonek.id,
            "przychod": "5000.00",
            "odpowiedz": self.status_odp.id,
            "opis": "Partner strategiczny"
        }
        response = self.client.post(self.url_partnerzy, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Partner.objects.count(), 1)
        self.assertEqual(Partner.objects.get().nazwa, "Tech Solutions Sp. z o.o.")

    def test_dodaj_partnera_nieistniejacy_czlonek(self):
        data = {
            "nazwa": "Błędna Firma",
            "osoba_odpowiedzialna": 9999,  # ID, które nie istnieje
            "przychod": "100.00",
            "odpowiedz": self.status_odp.id
        }
        response = self.client.post(self.url_partnerzy, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nie istnieje", str(response.data))


    def test_brak_nazwy_partnera(self):
        data = {
            "osoba_odpowiedzialna": self.czlonek.id,
            "przychod": "500.00",
            "odpowiedz": self.status_odp.id
        }
        response = self.client.post(self.url_partnerzy, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nazwa', response.data)
