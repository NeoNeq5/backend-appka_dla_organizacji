from rest_framework import serializers
from .models import Czlonek, WidokBazyCzlonkow, Kierunek, Czlonekkierunek

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

# Do przypisywania kierunku
class CzlonekKierunekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Czlonekkierunek
        fields = '__all__'