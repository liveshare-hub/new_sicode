from collections import namedtuple
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views
# from .views import nppAutoComplete

urlpatterns = [
    path('', views.index, name='home'),
    path('list/kpj/', views.listKPJ, name='list-kpj'),
    path('daftar/tk/', views.TambahTK, name='add-tk'),
    path('daftar/kpj/<int:pk>/', views.tambahKPJ, name='add-kpj'),
    path('input/kpj/', views.formDaftarKPJ, name='daftar-kpj'),
    path('input/kpj/ajax', views.daftarKPJ, name='daftar-kpj-ajax'),
    path('daftar/', views.tambahKlaim1, name='add'),
    path('pengkinian/json/', views.PengkinianJson, name='pengkinian-json'),
    path('pengkinian/hrd/', views.DaftarTk, name='hrd-tk'),
    path('pengkinian/tk/', views.ListDataTerkini, name='list-pengkinian'),
    path('pengkinian/tk/<int:pk>', views.PengkinianTK, name='pengkinian-tk'),
    path('hrd/klaim/', views.get_detail_tk, name='get-detail'),
    path('klaim/tk/<int:pk>', views.PengajuanKlaim, name='pengajuan-klaim-tk'),
    path('daftar/kpj/json/', views.DataTKJson, name='tk-json'),
    path('hrd/klaim/<int:klaim_id>/',
         views.get_klaimhrd_json, name='klaim-detail'),
    path('qr-code/<str:uid>/', views.detail_tk, name='detail-tk'),
    path('email/<int:id>/sent/', views.sent_mail, name='sent-mail'),
    # re_path(
    #     r'^npp-autocomplete/$',
    #     nppAutoComplete.as_view(),
    #     name='npp-autocomplete',
    # ),

]
