from rest_framework import serializers
from .models import Perusahaan

class PerusahaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perusahaan
        fields = '__all__'
        
