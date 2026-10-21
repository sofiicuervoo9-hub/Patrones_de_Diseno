# Escenario C · Proveedores externos

**Consigna:** combinar 3 o 4 patrones para resolver todo lo siguiente:

1. Integrar tres aerolíneas con APIs distintas y no modificables.
2. El viajero elige cómo comparar (precio, duración) en el momento de buscar.
3. Una sola operación «buscar y reservar» oculta consultar, bloquear y cobrar.
4. El conector correcto se crea a partir de un nombre.

| Pregunta | Respuesta del grupo |
|---|---|
| **Patrones elegidos (3 o 4)** | **Adapter, Factory Method, Facade, Strategy**<br>• **Adapter:** `LatamAdapter`, `AerolineasAdapter` y `FlybondiAdapter` traducen las tres APIs no modificables a la interfaz común `ProveedorAdapter`.<br>• **Factory Method:** `AdaptadorFactory` recibe el nombre del proveedor y crea el Adapter concreto correspondiente.<br>• **Facade:** `OperacionReservaFacade.buscarYReservar()` es la única operación que ve el viajero; oculta consultar, bloquear y cobrar.<br>• **Strategy:** el viajero elige al buscar una `EstrategiaComparacion` (`PorPrecio` o `PorDuracion`) y la fachada la usa para ordenar. |
| **Dibujo (cajas y flechas)** | Ver [diagrama](#dibujo-cajas-y-flechas) más abajo. |
| **Dos patrones que se combinan y cómo** | **Factory Method + Adapter:** la Factory (`AdaptadorFactory`) recibe un identificador con el nombre del proveedor (ej. `"LATAM"`) y devuelve la instancia del Adapter concreto (`LatamAdapter`). El Facade interactúa con el adaptador únicamente a través de la interfaz común `ProveedorAdapter`, desacoplándose por completo de las implementaciones concretas de cada API. |
| **Un patrón que descartaron y por qué** | **Abstract Factory:** se usa para instanciar familias de objetos relacionados o dependientes. En este escenario solo necesitamos instanciar un único objeto conector (Adapter) según un nombre dado, responsabilidad adecuada para Factory Method.<br><br>**Singleton:** no resuelve la instanciación de distintas clases concretas según un parámetro dinámico; solo garantiza una única instancia global de una clase específica, sumando además estado global y dificultando las pruebas unitarias. |
| **Cuando llegue el giro: ¿qué cambia y qué NO se toca?** | **Qué cambia (Hipótesis 1, sumar una nueva aerolínea):** se crea una nueva clase `NuevoProveedorAdapter` que implementa `ProveedorAdapter` y se agrega su caso en `AdaptadorFactory`.<br>**Qué cambia (Hipótesis 2, límite/costo de consultas a la API):** se agrega un Proxy con caché envolviendo a los adaptadores para reducir llamadas a las APIs externas.<br>**Qué NO se toca:** el código cliente (Viajero), `OperacionReservaFacade`, las estrategias de ordenamiento (Strategy) y los adaptadores existentes, respetando el principio Abierto/Cerrado (OCP). |

## Dibujo (cajas y flechas)

```
[ Cliente / Viajero ]
        │ buscarYReservar(origen, destino, criterio)
        ▼
[ OperacionReservaFacade ] ◀── FACADE: una sola operación
   │
   ├── 1 pide conector ────────▶ [ AdaptadorFactory ] ◀── FACTORY METHOD: «crea» el Adapter concreto
   │     por nombre                      │ devuelve       según el nombre, ej. crear("LATAM")
   │                                     ▼
   ├── 2 consulta ─────────────▶ [ ProveedorAdapter ] «interfaz»
   │   4 bloquea                         △ implementan
   │                 ┌───────────────────┼────────────────────┐
   │          [ LatamAdapter ] [ AerolineasAdapter ] [ FlybondiAdapter ] ◀── ADAPTER
   │                 │ traduce           │ traduce            │ traduce
   │                 ▼                   ▼                    ▼
   │            (API LATAM)      (API Aerolíneas)      (API Flybondi)  ← no modificables
   │
   ├── 3 ordena ───────────────▶ [ EstrategiaComparacion ] «interfaz» ◀── STRATEGY
   │                                 △                △
   │                           [ PorPrecio ]   [ PorDuracion ]
   │
   └── 5 cobra ────────────────▶ [ PasarelaPago ]
```

Implementación en Python: [`codigo/escenario_c.py`](../codigo/escenario_c.py).
