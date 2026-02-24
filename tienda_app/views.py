import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View

# Importaciones de modelos
from .models import Libro, Inventario, Orden

# Importaciones de arquitectura (Tutorial 02: Patrones Creacionales)
from .infra.factories import PaymentFactory
from .services import CompraService


# PASO 1: VISTA SPAGHETTI (FBV) - Para evidencia de contraste

def compra_rapida_fbv(request, libro_id):
    """
    Codigo inicial con logica mezclada (Violacion SRP y DIP).
    """
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        inventario = Inventario.objects.get(libro=libro)
        if inventario.cantidad > 0:
            total = float(libro.precio) * 1.19
            # Log de la version vieja
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


# PASO 2 Y 3: VISTA EMPRESARIAL (CBV + SERVICE LAYER + PATRONES)

class CompraView(View):
    """
    Vista Profesional Basada en Clases (CBV).
    Agnostica al procesador de pagos gracias al Factory Method.
    """
    template_name = 'tienda_app/compra_rapida.html'

    def setup_service(self):
        """
        Inyeccion de Dependencias:
        Obtiene el procesador (Real o Mock) desde la Fabrica segun el entorno.
        """
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        # Carga la interfaz con los datos del producto
        servicio = self.setup_service()
        try:
            contexto = servicio.obtener_detalle_producto(libro_id)
            return render(request, self.template_name, contexto)
        except Exception as e:
            return render(request, self.template_name, {'error': f"Error: {str(e)}"})

    def post(self, request, libro_id):
        servicio = self.setup_service()
        # Mantenemos el contexto cargado para el re-renderizado
        contexto = servicio.obtener_detalle_producto(libro_id)
        
        try:
            # Delegamos al Servicio (que ahora usa el OrdenBuilder actualizado)
            # Nota: El servicio internamente convertira el libro en una lista para el Builder
            total_final = servicio.ejecutar_compra(
                libro_id=libro_id, 
                cantidad=1,
                usuario=request.user if request.user.is_authenticated else None
            )
            
            contexto['mensaje_exito'] = "¡Exito! Compra procesada con patrones creacionales."
            contexto['total'] = total_final 
            
            return render(request, self.template_name, contexto)

        except (ValueError, Exception) as e:
            # Captura errores de stock, de validacion del Builder o de pasarela
            contexto['error'] = str(e)
            return render(request, self.template_name, contexto, status=400)