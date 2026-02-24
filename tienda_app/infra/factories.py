import os

from .gateways import BancoNacionalProcesador


class MockPaymentProcessor:
    def pagar(self, monto: float) -> bool:
        print(f"[DEBUG] Mock Payment: Procesando pago de ${monto} sin cargo real.")
        return True


from .gateways import BancoNacionalProcesador

class PaymentFactory:
    @staticmethod
    def get_processor():
        # Devuelve la instancia del procesador que acabas de editar
        return BancoNacionalProcesador()
