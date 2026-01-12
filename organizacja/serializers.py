from rest_framework import serializers
from .models import Czlonek, WidokBazyCzlonkow, Kierunek, Czlonekkierunek, Sekcja, Czloneksekcji, Czlonekprojektu, \
    Projekt, Partner, WidokPartnerow, OdpowiedziSlownik, Przychod, WidokBudzetu, Wydatek


# Słowniki
class OdpowiedziSlownikSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdpowiedziSlownik
        fields = ['id', 'nazwa']


# Moduł członków
class WidokBazyCzlonkowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidokBazyCzlonkow
        fields = '__all__'


class CzlonekSerializer(serializers.ModelSerializer):
    kierunek = serializers.IntegerField(required=False, write_only=True)
    sekcja = serializers.IntegerField(required=False, write_only=True)
    projekt = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Czlonek
        fields = ['id', 'imie', 'nazwisko', 'e_mail', 'indeks', 'telefon', 'opis', 'kierunek', 'sekcja', 'projekt']


class CzlonekKierunekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Czlonekkierunek
        fields = '__all__'


class KierunekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kierunek
        fields = '__all__'


class SekcjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sekcja
        fields = '__all__'


class CzlonekSekcjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Czloneksekcji
        fields = '__all__'


class ProjektSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projekt
        fields = '__all__'


class CzlonekProjektuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Czlonekprojektu
        fields = '__all__'

# Moduł partnerów
class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class WidokPartnerowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidokPartnerow
        fields = '__all__'

class OdpowiedziSlownikSerializer(serializers.ModelSerializer):
    class Meta:
        model = OdpowiedziSlownik
        fields = '__all__'



# Moduł budżetu
class CzlonekSzczegolySerializer(serializers.ModelSerializer):
    """Pomocniczy serializer do wyświetlania danych osoby w budżecie"""
    class Meta:
        model = Czlonek
        fields = ['imie', 'nazwisko', 'e_mail']


class PrzychodSerializer(serializers.ModelSerializer):
    osoba_dane = CzlonekSzczegolySerializer(source='osoba_odpowiedzialna', read_only=True)

    class Meta:
        model = Przychod
        fields = ['id', 'kwota', 'nazwa', 'data', 'osoba_odpowiedzialna', 'osoba_dane', 'id_partner', 'opis']


class WydatekSerializer(serializers.ModelSerializer):
    osoba_dane = CzlonekSzczegolySerializer(source='osoba_odpowiedzialna', read_only=True)

    class Meta:
        model = Wydatek
        fields = ['id', 'kwota', 'nazwa', 'data', 'osoba_odpowiedzialna', 'osoba_dane', 'opis']


class WidokBudzetuSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidokBudzetu
        fields = '__all__'

