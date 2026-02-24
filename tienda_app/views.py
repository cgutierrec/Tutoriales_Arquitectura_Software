import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View

# Importaciones de modelos
from .models import Libro, Inventario, Orden

# Importaciones de arquitectura (Paso 3)
from .infra.factories import PaymentFactory
from .services import CompraService


# PASO 1: VISTA SPAGHETTI (FBV) - Para evidencia de contraste

def compra_rapida_fbv(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        inventario = Inventario.objects.get(libro=libro)
        if inventario.cantidad > 0:
            total = float(libro.precio) * 1.19
            # Log de la versión vieja
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
    Vista Profesional Basada en Clases.
    Utiliza Inyección de Dependencias y Capa de Servicio.
    """
    template_name = 'tienda_app/compra_rapida.html'

    def setup_service(self):
        # La Factory decide qué procesador usar (Infraestructura)
        gateway = PaymentFactory.get_processor()
        # El Servicio orquesta la lógica (Service Layer)
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        # Carga la página limpia por primera vez
        servicio = self.setup_service()
        try:
            contexto = servicio.obtener_detalle_producto(libro_id)
            return render(request, self.template_name, contexto)
        except Exception as e:
            return render(request, self.template_name, {'error': f"Producto no encontrado: {str(e)}"})

    def post(self, request, libro_id):
        servicio = self.setup_service()
        # Primero obtenemos los datos del producto para poder re-renderizar la página
        contexto = servicio.obtener_detalle_producto(libro_id)
        
        try:
            # Ejecutamos la compra
            total_final = servicio.ejecutar_compra(
                libro_id=libro_id, 
                cantidad=1,
                usuario=request.user if request.user.is_authenticated else None
            )
            
            # Añadimos el mensaje de éxito al contexto existente
            contexto['mensaje_exito'] = "¡Éxito! Compra procesada vía Service Layer (SOLID)."
            contexto['total'] = total_final # Actualizamos con el valor real del Builder
            
            return render(request, self.template_name, contexto)

        except (ValueError, Exception) as e:
            # Si algo falla (ej. sin stock), mandamos el error pero mantenemos la info del libro
            contexto['error'] = str(e)
            return render(request, self.template_name, contexto, status=400)