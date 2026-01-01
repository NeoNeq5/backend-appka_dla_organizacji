from rest_framework import serializers
from .models import Czlonek, WidokBazyCzlonkow, Kierunek, Czlonekkierunek, Sekcja, Czloneksekcji, Czlonekprojektu, \
    Projekt


# Lista członków
class WidokBazyCzlonkowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidokBazyCzlonkow
        fields = '__all__'


# CRUD
class CzlonekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Czlonek
        fields = ['id', 'imie', 'nazwisko', 'e_mail', 'indeks', 'telefon', 'opis']


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