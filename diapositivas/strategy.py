from abc import ABC, abstractmethod


# Un vuelo con nombre, precio y duración
class Vuelo:
    def __init__(self, nombre, precio, minutos):
        self.nombre = nombre
        self.precio = precio
        self.minutos = minutos


# Interfaz común: todas las estrategias saben "ordenar"
class EstrategiaOrden(ABC):
    @abstractmethod
    def ordenar(self, vuelos):
        pass


# Estrategia 1: del más barato al más caro
class PorPrecio(EstrategiaOrden):
    def ordenar(self, vuelos):
        return sorted(vuelos, key=lambda v: v.precio)


# Estrategia 2: del más corto al más largo
class PorDuracion(EstrategiaOrden):
    def ordenar(self, vuelos):
        return sorted(vuelos, key=lambda v: v.minutos)


# Contexto: guarda la estrategia elegida y le delega el orden
class Buscador:
    def __init__(self, vuelos):
        self.vuelos = vuelos
        self.criterio = None

    def set_criterio(self, criterio):
        self.criterio = criterio          # reemplaza el criterio anterior

    def resultados(self):
        return self.criterio.ordenar(self.vuelos)


# ---------- Prueba (lo que muestra la diapositiva) ----------
A = Vuelo("A", 300, 120)
B = Vuelo("B", 250, 300)
C = Vuelo("C", 400, 90)

bu = Buscador([A, B, C])
bu.set_criterio(PorPrecio())
bu.set_criterio(PorDuracion())            # pisa a PorPrecio
print(bu.resultados()[0].nombre)          # C