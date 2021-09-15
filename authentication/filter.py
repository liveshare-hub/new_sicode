from django_filters import rest_framework as filters
from rest_framework import generics
from .serializer import PerusahaanSerializer

from .models import Perusahaan

class PerusahaanFilter(filters.FilterSet):
    class Meta:
        model = Perusahaan
        fields = {
            'npp': ['exact',],
        }

class PerusahaanList(generics.ListAPIView):
    queryset = Perusahaan.objects.all()
    serializer_class = PerusahaanSerializer
    filterset_class = PerusahaanFilter