from django.urls import path
from .views import TronTxView


urlpatterns = [
    path("tx/<str:txid>/", TronTxView.as_view(), name="tron_tx"),
]