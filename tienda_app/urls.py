from django.urls import path
from .api.views import CompraAPIView
from .views import CompraView
from tienda_app.views import compra_rapida_fbv, CompraView # Importa ambas

urlpatterns = [
    # Usamos .as_view() para habilitar la CBV
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    path('compra-fbv/<int:libro_id>/', compra_rapida_fbv, name='compra_rapida_fbv'),
    path('compra-cbv/<int:libro_id>/', CompraView.as_view(), name='compra_cbv'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]