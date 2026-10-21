from abc import ABC, abstractmethod


# Clase padre: define el esqueleto fijo
class Voucher(ABC):
    def emitir(self):
        # Los 4 pasos, siempre en el mismo orden
        return ["validar", "cobrar", "generar:" + self.generar(), "enviar"]

    @abstractmethod
    def generar(self):
        pass                               # el único paso que cambia


# Subclase: solo completa el paso que cambia
class VoucherMicro(Voucher):
    def generar(self):
        return "MICRO"


# Respuesta a los huecos: (1) Voucher  (2) generar
class VoucherHotel(Voucher):
    def generar(self):
        return "HOTEL"


# ---------- Prueba (lo que muestra la diapositiva) ----------
print(VoucherMicro().emitir())   # ['validar', 'cobrar', 'generar:MICRO', 'enviar']
print(VoucherHotel().emitir())   # ['validar', 'cobrar', 'generar:HOTEL', 'enviar']
