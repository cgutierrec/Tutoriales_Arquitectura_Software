from ..models import Orden
from decimal import Decimal

class OrdenBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario = None
        self._items = []  # Lista de productos segun el tutorial
        self._direccion = ""

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self

    def con_productos(self, productos):
        # Acepta una lista de objetos libro
        self._items = productos
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        if not self._items:
            raise ValueError("No hay productos seleccionados para la orden.")

        # Extraemos el primer libro para cumplir con la base de datos (NOT NULL constraint)
        libro_principal = self._items[0]

        # Calculo de totales (Decimal para precision financiera)
        subtotal = sum(Decimal(str(p.precio)) for p in self._items)
        total_con_iva = subtotal * Decimal('1.19')

        # Creamos la orden con el libro_id que la base de datos exige
        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=libro_principal,  # <--- Esto evita el error de NOT NULL
            total=total_con_iva,
            direccion_envio=self._direccion
        )
        
        self.reset()
        return orden