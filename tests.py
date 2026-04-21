import datetime
from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    def pagar(self, monto: float) -> bool:
        # AQUÍ pones tu nombre real. Este archivo se crea en la raíz del proyecto.
        archivo_log = "pagos_locales_CRISTOBAL_Gutierrez.log"
        
        with open(archivo_log, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Transacción exitosa por: ${monto}\n")
        return True