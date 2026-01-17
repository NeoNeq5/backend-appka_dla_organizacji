from rest_framework import status
from rest_framework.test import APITestCase
from .models import Czlonek


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


