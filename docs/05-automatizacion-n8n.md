# 05. Automatización vinculada al BPMN TO-BE

## 1. Componente implementado

La pauta admite n8n u otra herramienta equivalente. En esta entrega se implementó una **automatización local en Python y SQLite**, no un flujo n8n instalado. Sus operaciones son reproducibles desde `scripts/automatizacion_local.py` o desde la interfaz de `prototipo_web/`.

**Tarea automatizada:** comparar el material indicado por el identificador QR de una bobina con el material requerido en la orden; registrar el intento y, según el resultado, crear un retiro pendiente o emitir una alerta. La segunda lectura vuelve a comparar orden, bobina y retiro.

## 2. Entradas y resultados

| Entrada | Descripción |
|---|---|
| `etapa` | `BODEGA` o `PRODUCCION` |
| `orden` | Código de orden de producción existente |
| `codigo_qr` | Identificador único de bobina |
| `usuario` | Código del responsable de la etapa |
| `retiro_id` | Obligatorio solo en producción |

| Situación | Registro guardado | Decisión |
|---|---|---|
| Bodega: bobina equivocada | Validación `NO_COINCIDE` | No se crea retiro |
| Bodega: bobina correcta y disponible | Validación `COINCIDE` + retiro | Queda `PENDIENTE`; bobina `RESERVADA` |
| Producción: QR distinto | Validación `NO_COINCIDE` | Se mantiene pendiente |
| Producción: mismo QR y orden | Validación `COINCIDE` | Retiro `CONFIRMADO`; bobina `ENTREGADA` |

Se distingue **entrega** de **consumo** porque el modelo no observa cuántos metros se utilizan en impresión.

## 3. Instrucciones de reproducción

Partir de una base nueva creada con `python scripts/crear_base.py`. Luego:

```bash
# Caso erróneo: genera alerta y bloquea
python scripts/automatizacion_local.py db/colorink_demo.sqlite BODEGA OP-2026-013 BOB-014 US-B01

# Caso correcto: crea el retiro pendiente
python scripts/automatizacion_local.py db/colorink_demo.sqlite BODEGA OP-2026-013 BOB-013 US-B01

# Validación final, usando el ID real que imprimió el paso anterior
python scripts/automatizacion_local.py db/colorink_demo.sqlite PRODUCCION OP-2026-013 BOB-013 US-P01 13
```

La misma secuencia se puede observar desde `http://127.0.0.1:8765` después de ejecutar `python prototipo_web/servidor.py`.

## 4. Cómo corresponde cada actividad al BPMN

| BPMN | Ejecución verificable |
|---|---|
| Lectura de bobina | Campo de identificador QR o lector tipo teclado |
| Consultar material de la orden | SELECT de `ordenes_produccion` |
| Consultar material de la bobina | SELECT de `bobinas` |
| Comparar y decidir | Función `registrar_lectura` + trigger de integridad |
| Registrar alerta | INSERT en `validaciones`, resultado NO_COINCIDE |
| Crear retiro | INSERT en `retiros` con referencia a validación de bodega |
| Confirmar entrega | Segunda validación de producción; trigger de cambio de estado |

## 5. Equivalencia con un eventual flujo n8n

Un flujo n8n futuro podría iniciar con un Webhook interno, recibir orden/QR/usuario, consultar el servicio de validación y bifurcar mediante un nodo de condición. La rama incompatible respondería con la alerta registrada; la rama conforme permitiría registrar el retiro. Un segundo Webhook vinculado al retiro resolvería la recepción en producción. Los controles de integridad deben mantenerse en el servidor y la base, no depender solo de una decisión en la interfaz gráfica.

No se incluye un archivo JSON exportado de n8n porque tal despliegue **no se realizó**. La alternativa homóloga aportada es código fuente ejecutable y documentación suficiente para reproducirla.

## 6. Restricciones técnicas

El prototipo funciona solo en localhost y no incorpora inicio de sesión, permisos reales por credenciales, HTTPS ni control de concurrencia de producción. El campo QR no utiliza cámara. Las operaciones se realizan sobre datos sintéticos. Son restricciones importantes de cara a un piloto en Colorink.
