# Código de las diapositivas

## Diapositiva 24 · Código 21: Strategy («Cambiar el criterio de orden»)

**Respuestas**
- a) Se imprime **C**.
- b) `Buscador` es el **contexto**.

**Explicación**
1. `Buscador` guarda los vuelos A, B y C.
2. `set_criterio(PorPrecio())` elige ordenar por precio.
3. `set_criterio(PorDuracion())` **reemplaza** al anterior, así que solo queda la duración.
4. Al ordenar por duración, el más corto es **C (90 min)**.

Código: [`strategy.py`](strategy.py) · Salida: `C`

## Diapositiva 25 · Código 22: Template Method («Esqueleto del voucher»)

**Respuestas**
- a) La lista tiene **4 pasos**: `['validar', 'cobrar', 'generar:MICRO', 'enviar']`
- b) (1) **Voucher**, (2) **generar**

```python
class VoucherHotel(Voucher):
    def generar(self): return "HOTEL"
```

**Explicación**
1. La clase padre `Voucher` tiene el método `emitir()`, que fija siempre los mismos 4 pasos y en el mismo orden: validar, cobrar, generar y enviar.
2. De esos pasos, el único que cambia según el tipo de voucher es `generar()`.
3. `VoucherMicro` completa ese paso con `"MICRO"`, y por eso la lista dice `'generar:MICRO'`.
4. Para el hotel se hace lo mismo: se hereda de `Voucher` (1) y se escribe solo `generar` (2).

Código: [`template_method.py`](template_method.py)

## Cómo ejecutar

```bash
python diapositivas/strategy.py
python diapositivas/template_method.py
```
