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

        # czy nazwisko się zgadza
        self.assertEqual(Czlonek.objects.get().nazwisko, "Kowalski")

        #czy indeks jest liczbą
        self.assertIsInstance(Czlonek.objects.get().indeks, int)

        #czy telefon jest liczbą
        self.assertIsInstance(Czlonek.objects.get().telefon, int)

        # czy obie wartości są poprawne
        self.assertContains(response, 'Jan', status_code=status.HTTP_201_CREATED)

        # czy odpowiedź zawiera wszystkie poprawne dane
        self.assertJSONEqual(response.content, {'e_mail': 'jan.kowalski@test.pl', 'id': 1, 'imie': 'Jan', 'indeks': 112233,
                                                'nazwisko': 'Kowalski', 'opis': None, 'telefon': 123456789})

        # czy e-mail się zgadza
        self.assertTrue(Czlonek.objects.filter(e_mail="jan.kowalski@test.pl").exists())


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

        # czy wykryje duplikat indeksu
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_brak_wymaganych_pol(self):
        data = {
            "e_mail": "tylko_email@test.pl"
        }
        response = self.client.post(self.url, data, format='json')

        # sprawdza czy zwraca błąd dla brakujących pól
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # sprawdza czy odpowiedź zawiera informacje o brakujących polach
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

        #czy imię przekraczające limit znaków jest odrzucone
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # czy odpowiedź zawiera informację o limicie znaków
        self.assertIn('imie', response.data)

    def test_dodaj_czlonka_minimalne_dane(self):
        data = {
            "imie": "Maria",
            "nazwisko": "Nowak",
            "e_mail": "m.nowak@test.pl"
            # brak indeksu i telefonu
        }
        response = self.client.post(self.url, data, format='json')

        # czy członek został dodany pomyślnie
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        czlonek = Czlonek.objects.get(e_mail="m.nowak@test.pl")

        # czy indeks są None
        self.assertIsNone(czlonek.indeks)

        # czy telefon jest None
        self.assertIsNone(czlonek.telefon)

    def test_puste_wartosci_wymagane(self):
        data = {
            "imie": "",
            "nazwisko": "",
            "e_mail": ""
        }
        response = self.client.post(self.url, data, format='json')

        # czy puste wartości są odrzucone
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # czy zwróci błędy dla wszystkich trzech pól
        for field in ['imie', 'nazwisko', 'e_mail']:
            self.assertIn(field, response.data)


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

        # czy odpowiedź jest poprawna
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Oczekiwane saldo: 100 - 30 = 70

        # czy saldo jest poprawne
        self.assertEqual(float(response.data['saldo']), 70.00)

        # czy saldo jest poprawne z dokładnością do 2 miejsc po przecinku
        self.assertAlmostEqual(float(response.data['saldo']), 70.00, places=2)

        # czy suma przychodów jest poprawna
        self.assertEqual(float(response.data['suma_przychodow']), 100.00)

        # czy suma wydatków jest poprawna
        self.assertEqual(float(response.data['suma_wydatkow']), 30.00)

        # czy obie wartości są poprawne
        self.assertContains(response, 'saldo', status_code=status.HTTP_200_OK)

        self.assertContains(response, 'suma_przychodow', status_code=status.HTTP_200_OK)

    def test_wydatek_bez_osoby_odpowiedzialnej(self):
        data = {
            "kwota": "10.00",
            "nazwa": "Błąd",
            "data": timezone.now().isoformat()
            # Brak osoba_odpowiedzialna
        }
        response = self.client.post(self.url_wydatek, data, format='json')

        #czy brak osoby odpowiedzialnej zwraca błąd
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_uzycie_tekstu_zamiast_kwoty(self):
        data = {
            "kwota": "za_duzo_pieniedzy",
            "nazwa": "Błąd",
            "data": timezone.now().isoformat(),
            "osoba_odpowiedzialna": self.osoba.id
        }
        response = self.client.post(self.url_przychod, data, format='json')

        # czy użycie tekstu zamiast liczby zwraca błąd
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # czy odpowiedź zawiera informacje o błędnej kwocie
        self.assertIn('kwota', response.data)

class PartnerAPITests(APITestCase):
    def setUp(self):
        # członek, który będzie osobą odpowiedzialną
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

        self.valid_payload = {
            "nazwa": "Firma Testowa",
            "numer_telefonu": 123456789,
            "e_mail": "kontakt@firma.pl",
            "osoba_odpowiedzialna": self.czlonek.id,
            "przychod": "1500.00",
            "odpowiedz": self.status_odp.id
        }

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

        # czy partner został dodany pomyślnie
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # czy jest 1 rekord partnera
        self.assertEqual(Partner.objects.count(), 1)

        # czy nazwa partnera się zgadza
        self.assertEqual(Partner.objects.get().nazwa, "Tech Solutions Sp. z o.o.")

        # czy numer telefonu się zgadza
        self.assertEqual(Partner.objects.get().numer_telefonu, 555666777)

        #czy e-mail się zgadza
        self.assertEqual(Partner.objects.get().e_mail, "biuro@techsolutions.pl")

        # czy przychód się zgadza
        self.assertEqual(float(Partner.objects.get().przychod), 5000.00)

        # czy opis się zgadza
        self.assertEqual(Partner.objects.get().opis, "Partner strategiczny")

        # czy przychód jest poprawny z dokładnością do 2 miejsc po przecinku
        self.assertAlmostEqual(float(Partner.objects.get().przychod), 5000.00)

    def test_dodaj_partnera_nieistniejacy_czlonek(self):
        data = {
            "nazwa": "Błędna Firma",
            "osoba_odpowiedzialna": 9999,  # ID, które nie istnieje
            "przychod": "100.00",
            "odpowiedz": self.status_odp.id
        }
        response = self.client.post(self.url_partnerzy, data, format='json')

        # czy zwraca błąd przy dodaniu nieistniejącego członka jako osoby odpowiedzialnej
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # czy odpowiedź zawiera informację o nieistniejącym członku
        self.assertIn("nie istnieje", str(response.data))


    def test_brak_nazwy_partnera(self):
        data = {
            "osoba_odpowiedzialna": self.czlonek.id,
            "przychod": "500.00",
            "odpowiedz": self.status_odp.id
        }
        response = self.client.post(self.url_partnerzy, data, format='json')

        # czy brak nazwy partnera zwraca błąd
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # czy odpowiedź zawiera informację o brakującej nazwie
        self.assertIn('nazwa', response.data)

    def test_dodaj_partnera_minimalne_dane(self):
        data = {
            "nazwa": "Minimalistyczna Firma",
            "osoba_odpowiedzialna": self.czlonek.id,
            "przychod": "0.00",
            "odpowiedz": self.status_odp.id
        }
        response = self.client.post(self.url_partnerzy, data, format='json')

        # czy partner został dodany pomyślnie
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        partner = Partner.objects.get(nazwa="Minimalistyczna Firma")

        # czy e-mail jest None
        self.assertIsNone(partner.e_mail)

        # czy numer telefonu jest None
        self.assertIsNone(partner.numer_telefonu)

    def test_limit_znakow_nazwa_partnera(self):
        data = self.valid_payload.copy()
        data["nazwa"] = "P" * 101

        response = self.client.post(self.url_partnerzy, data, format='json')

        # czy nazwa partnera przekraczająca limit znaków jest odrzucona
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # czy odpowiedź zawiera informację o błędzie w nazwie
        self.assertIn('nazwa', response.data)

    def test_niepoprawny_format_przychod(self):
        data = self.valid_payload.copy()
        data["przychod"] = "duzo_pieniedzy"

        response = self.client.post(self.url_partnerzy, data, format='json')

        # czy niepoprawny format przychodu zwraca błąd
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




