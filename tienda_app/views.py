import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View

# Importaciones de modelos
from .models import Libro, Inventario, Orden

# Importaciones para la arquitectura limpia (Paso 3)
from .infra.factories import PaymentFactory
from .services import CompraService


# PASO 1: VISTA SPAGHETTI (FBV)

def compra_rapida_fbv(request, libro_id):
    """
    Punto de partida desordenado. 
    Violaciones: SRP (Lógica en vista), OCP (Cálculo hardcoded), DIP (Acoplado a log).
    """
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        # VIOLACIÓN SRP: Lógica de inventario en la vista
        inventario = Inventario.objects.get(libro=libro)
        if inventario.cantidad > 0:
            # VIOLACIÓN OCP: Cálculo de negocio hardcoded
            total = float(libro.precio) * 1.19

            # VIOLACIÓN DIP: Proceso de pago acoplado al file system
            with open("pagos_manuales.log", "a") as f:
                f.write(f"[{datetime.datetime.now()}] Pago FBV: ${total}\n")

            inventario.cantidad -= 1
            inventario.save()
            Orden.objects.create(libro=libro, total=total)

            return HttpResponse(f"Compra exitosa (FBV): {libro.titulo}")
        else:
            return HttpResponse("Sin stock", status=400)

    total_estimado = float(libro.precio) * 1.19
    return render(request, 'tienda_app/compra_rapida.html', {
        'libro': libro,
        'total': total_estimado
    })


# PASO 2 Y 3: VISTA EMPRESARIAL (CBV + SERVICE LAYER)

class CompraView(View):
    """
    CBV: Vista Basada en Clases desacoplada.
    Actúa como un "Portero": recibe la petición y delega al servicio.
    """
    template_name = 'tienda_app/compra_rapida.html' # Ajustado al template del tutorial

    def setup_service(self):
        # Inyección de dependencias mediante Factory
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        # El servicio se encarga de preparar los datos para la interfaz
        try:
            # Asumiendo que tu servicio tiene este método según tu código previo
            contexto = servicio.obtener_detalle_producto(libro_id)
            return render(request, self.template_name, contexto)
        except Exception:
            # Fallback en caso de que el método no exista aún en tu service.py
            libro = get_object_or_404(Libro, id=libro_id)
            total = float(libro.precio) * 1.19
            return render(request, self.template_name, {'libro': libro, 'total': total})

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            # El servicio orquesta la transacción completa
            total = servicio.ejecutar_compra(libro_id, cantidad=1)
            return render(
                request,
                self.template_name,
                {
                    'mensaje_exito': f"¡Gracias por su compra! Total: ${total}",
                    'total': total,
                },
            )
        except (ValueError, Exception) as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)