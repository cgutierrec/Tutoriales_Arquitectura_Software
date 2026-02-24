from django.shortcuts import get_object_or_404
from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro

class CompraService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}

    def ejecutar_compra(self, libro_id, cantidad=1, direccion="Calle Falsa 123", usuario=None):
        libro = get_object_or_404(Libro, id=libro_id)
        inv = get_object_or_404(Inventario, libro=libro)

        if inv.cantidad < cantidad:
            raise ValueError("No hay suficiente stock.")

        # Construcción de la orden usando el patrón Builder
        orden = (
            self.builder
            .con_usuario(usuario)
            .con_productos([libro])
            .para_envio(direccion) # Asegúrate de pasar una dirección por defecto
            .build()
        )

        if self.procesador_pago.pagar(orden.total):
            inv.cantidad -= cantidad
            inv.save()
            return orden.total
        
        orden.delete()
        raise Exception("Pago rechazado.")