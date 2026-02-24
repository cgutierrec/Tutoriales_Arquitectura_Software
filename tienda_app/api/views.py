from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdenInputSerializer
from tienda_app.services import CompraService
from tienda_app.infra.factories import PaymentFactory

class CompraAPIView(APIView):
    def post(self, request):
        # 1. Validacion de datos (Adapter)
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        datos = serializer.validated_data
        
        try:
            # 2. Reutilizacion de Factory y Service Layer
            gateway = PaymentFactory.get_processor()
            servicio = CompraService(procesador_pago=gateway)
            
            # 3. Ejecucion (La misma logica que la vista HTML)
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                direccion=datos['direccion_envio'],
                usuario=request.user if request.user.is_authenticated else None
            )
            
            return Response({
                "estado": "exito",
                "mensaje": f"Orden creada exitosamente. Total: {resultado}"
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)