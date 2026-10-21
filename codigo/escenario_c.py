"""ViajaYa - Escenario C: Proveedores externos (Grupo 11).

Patrones combinados:
  - Adapter:        LatamAdapter, AerolineasAdapter y FlybondiAdapter traducen tres APIs de aerolineas no modificables.
  - Strategy:       el viajero elige el criterio de comparacion (precio, duracion).
  - Facade:         OperacionReservaFacade.buscarYReservar() oculta consultar, bloquear y cobrar.
  - Factory Method: AdaptadorFactory.crear(nombre) devuelve el conector correcto.

Las clases Vuelo, PorPrecio, PorDuracion y Buscador siguen
la forma del codigo de referencia del curso (viajaya.py); EstrategiaComparacion
equivale a EstrategiaOrden.
"""
from abc import ABC, abstractmethod


# ======================================================================
# APIs externas de las aerolineas (NO MODIFICABLES: cada una distinta)
# ======================================================================
class ApiLatam:
    """Responde en XML."""
    def consultar_xml(self, origen, destino):
        return (f"<vuelos><vuelo cod='LA100' precio='300' min='120'/>"
                f"<vuelo cod='LA200' precio='280' min='200'/></vuelos>")
    def reservar_asiento(self, codigo):
        return f"<ok cod='{codigo}'/>"


class ApiAerolineas:
    """Responde diccionarios en ingles, precio en centavos y duracion en horas."""
    def get_flights(self, from_, to):
        return [{"code": "AR300", "price_cents": 25000, "hours": 5.0}]
    def hold(self, code):
        return {"status": "HELD", "code": code}


class ApiFlybondi:
    """Recibe la ruta como texto y devuelve tuplas (codigo, minutos, precio)."""
    def buscarVuelos(self, ruta):
        return [("FB400", 90, 400.0)]
    def bloquearPlaza(self, codigo, cantidad):
        return True


# ======================================================================
# Modelo (igual que viajaya.py, con la aerolinea de origen)
# ======================================================================
class Vuelo:
    def __init__(self, nombre, precio, minutos, escalas=0, puntaje=0, aerolinea=""):
        self.nombre, self.precio, self.minutos = nombre, precio, minutos
        self.escalas, self.puntaje, self.aerolinea = escalas, puntaje, aerolinea
    def __repr__(self):
        return f"{self.nombre} (${self.precio:.0f}, {self.minutos} min)"


# ======================================================================
# ADAPTER: interfaz comun + un adaptador por aerolinea
# ======================================================================
class ProveedorAdapter(ABC):
    @abstractmethod
    def buscar(self, origen, destino): ...      # -> list[Vuelo]
    @abstractmethod
    def bloquear(self, vuelo): ...              # -> bool


class LatamAdapter(ProveedorAdapter):
    def __init__(self): self._api = ApiLatam()
    def buscar(self, origen, destino):
        import xml.etree.ElementTree as ET
        raiz = ET.fromstring(self._api.consultar_xml(origen, destino))
        return [Vuelo(v.get("cod"), float(v.get("precio")), int(v.get("min")), aerolinea="LATAM")
                for v in raiz.findall("vuelo")]
    def bloquear(self, vuelo):
        return self._api.reservar_asiento(vuelo.nombre).startswith("<ok")


class AerolineasAdapter(ProveedorAdapter):
    def __init__(self): self._api = ApiAerolineas()
    def buscar(self, origen, destino):
        return [Vuelo(f["code"], f["price_cents"] / 100, int(f["hours"] * 60), aerolinea="AEROLINEAS")
                for f in self._api.get_flights(origen, destino)]
    def bloquear(self, vuelo):
        return self._api.hold(vuelo.nombre)["status"] == "HELD"


class FlybondiAdapter(ProveedorAdapter):
    def __init__(self): self._api = ApiFlybondi()
    def buscar(self, origen, destino):
        return [Vuelo(cod, precio, minutos, aerolinea="FLYBONDI")
                for cod, minutos, precio in self._api.buscarVuelos(f"{origen}-{destino}")]
    def bloquear(self, vuelo):
        return self._api.bloquearPlaza(vuelo.nombre, 1)


# ======================================================================
# FACTORY METHOD: el conector correcto a partir de un nombre
# ======================================================================
class AdaptadorFactory:
    _registro = {"LATAM": LatamAdapter, "AEROLINEAS": AerolineasAdapter, "FLYBONDI": FlybondiAdapter}

    def crear(self, nombre) -> ProveedorAdapter:
        if nombre not in self._registro:
            raise ValueError(f"Aerolinea desconocida: {nombre}")
        return self._registro[nombre]()


# ======================================================================
# STRATEGY: criterio de comparacion elegido por el viajero
# ======================================================================
class EstrategiaComparacion(ABC):
    @abstractmethod
    def ordenar(self, vuelos): ...

class PorPrecio(EstrategiaComparacion):
    def ordenar(self, v): return sorted(v, key=lambda x: x.precio)

class PorDuracion(EstrategiaComparacion):
    def ordenar(self, v): return sorted(v, key=lambda x: x.minutos)

class Buscador:                      # contexto
    def __init__(self, vuelos): self._v = vuelos; self._e = None
    def set_criterio(self, e): self._e = e
    def resultados(self): return self._e.ordenar(self._v)


# ======================================================================
# Pago (subsistema que usa la fachada)
# ======================================================================
class PasarelaPago(ABC):
    @abstractmethod
    def cobrar(self, monto): ...

class PagoSimulado(PasarelaPago):
    def cobrar(self, monto):
        print(f"  Cobrando ${monto:.2f}")
        return True


# ======================================================================
# FACADE: una sola operacion para el viajero
# ======================================================================
class OperacionReservaFacade:
    def __init__(self, aerolineas, pasarela: PasarelaPago):
        fabrica = AdaptadorFactory()
        self._conectores = {n: fabrica.crear(n) for n in aerolineas}   # 1. crear por nombre
        self._pasarela = pasarela

    def buscarYReservar(self, origen, destino, criterio: EstrategiaComparacion):
        vuelos = [v for c in self._conectores.values()                  # 2. consultar
                  for v in c.buscar(origen, destino)]
        if not vuelos:
            return None
        buscador = Buscador(vuelos)                                     # 3. ordenar
        buscador.set_criterio(criterio)
        elegido = buscador.resultados()[0]
        if not self._conectores[elegido.aerolinea].bloquear(elegido):   # 4. bloquear
            return None
        if not self._pasarela.cobrar(elegido.precio):                   # 5. cobrar
            return None
        return f"VOUCHER-{elegido.nombre}-{origen}-{destino}"


# ======================================================================
# Demo
# ======================================================================
if __name__ == "__main__":
    viaje = OperacionReservaFacade(["LATAM", "AEROLINEAS", "FLYBONDI"], PagoSimulado())

    print("Viajero elige comparar por PRECIO:")
    print(" ", viaje.buscarYReservar("MDZ", "BUE", PorPrecio()))

    print("Viajero elige comparar por DURACION:")
    print(" ", viaje.buscarYReservar("MDZ", "BUE", PorDuracion()))
