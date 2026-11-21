# Colorink | ICN-292, Entrega 2

**Sistemas de Información para la Gestión · UTFSM · Paralelo P100 · Segundo semestre de 2026**

**Integrantes:** Antonia Flores, Bastián Guajardo, Wan Lo Xie, Carolina Tavil y Mateo Vásquez.

**Caso de estudio:** Colorink, producción flexográfica de etiquetas.

**Repositorio definido por el equipo:** https://github.com/Wan-Lo-Xie/ICN292_Grupo1

> Este conjunto de archivos se preparó para agregarlo al repositorio original, sin crearlo ni modificarlo automáticamente. Su contenido se fundamenta en el informe de Entrega 1 y el enunciado de Entrega 2 facilitados por el equipo. **No se certifica el estado actual del repositorio remoto**, que debe comprobarse después de integrar la entrega.

## 1. Punto de partida y solución

En la Entrega 1 se documentó un problema de control en la transferencia de bobinas desde bodega a impresión. Una bobina distinta de la solicitada en la orden puede ingresar al proceso, y la discrepancia puede detectarse cuando ya existen costos de impresión o atrasos en las etapas siguientes. La propuesta de Entrega 2 formaliza dos lecturas del identificador QR: una antes de autorizar el retiro y otra al recibir material en producción. El sistema registra los intentos rechazados, conserva responsable y fecha, y confirma la entrega solo cuando ambas revisiones son satisfactorias.

El prototipo **no se ha integrado con Colorink**. Su base de datos y sus resultados son **enteramente sintéticos**. Los identificadores QR se ingresan mediante teclado o lector que se comporte como teclado; no hay reconocimiento de imágenes, verificación con cámara ni modelo de IA entrenado.

## 2. Contenido del proyecto

| Ruta | Contenido |
|---|---|
| `informe/` | Informe final, versiones idénticas en Word y PDF |
| `presentacion/` | Diapositivas PPTX/PDF y guion de defensa |
| `docs/` | Contexto del caso, requerimientos, BPMN, datos, SQL y automatización |
| `assets/` | Modelo BPMN 2.0 editable, figuras, modelo E/R y catálogo de QR de prueba |
| `db/schema.sql` | Siete tablas, restricciones referenciales y disparadores |
| `db/seed.sql` | Datos de demostración para reproducir las consultas |
| `db/consultas/` | Cinco consultas de negocio, ejecutables individualmente |
| `scripts/` | Generación de base, servicio de validación, pruebas y exportación de resultados |
| `prototipo_web/` | Interfaz de localhost sin dependencias externas |
| `evidencias/` | CSV de salida calculados sobre el conjunto sintético |
| `DECLARACION_IA.md` y `CHANGELOG.md` | Transparencia y cambios frente a la E1 |

## 3. Requisitos del equipo

- Python **3.10 o superior**, con `sqlite3` integrado.
- Navegador actual (opcional, solo para abrir la interfaz).
- Sistema Windows, macOS o Linux.
- No se requiere instalar MySQL, Flask, paquetes `pip` ni n8n.

**Motor SQL utilizado: SQLite 3.** La pauta permite el uso de SQL; el archivo `schema.sql` incluye disparadores específicos de SQLite y **no debe importarse a MySQL sin adaptación**.

## 4. Instalación desde una copia limpia

Una vez que el equipo haya incorporado los archivos E2 a la rama que defenderá, abrir una terminal y ejecutar:

```bash
git clone https://github.com/Wan-Lo-Xie/ICN292_Grupo1.git
cd ICN292_Grupo1
python scripts/verificar_entrega.py
python scripts/crear_base.py
python scripts/ejecutar_consultas.py
python scripts/exportar_resultados.py
```

En Windows, `py -3` puede reemplazar a `python`. Si se trabaja solo con el ZIP antes de publicarlo, abrir la terminal directamente en la carpeta `ICN292_E2_Colorink` y ejecutar los cuatro comandos Python.

**No repetir `crear_base.py` sobre una base ya existente:** se niega a sobrescribirla por diseño. Para restablecer el escenario inicial, cerrar el servidor, eliminar exclusivamente el archivo generado `db/colorink_demo.sqlite` y crear una base nueva.

## 5. Demostración visual en localhost

Con la base ya creada:

```bash
python prototipo_web/servidor.py
```

Abrir `http://127.0.0.1:8765` en el mismo computador. El servidor se detiene con `Ctrl+C`.

**Demostración guiada (la base se modifica):**

1. En Bodega, seleccionar la orden `OP-2026-013`, ingresar `BOB-014` y utilizar `US-B01`. El material no coincide: aparece una alerta y **no se crea retiro**.
2. Con la misma orden y usuario, ingresar `BOB-013`. Se crea un retiro **PENDIENTE** y la bobina queda **RESERVADA**.
3. En Producción, seleccionar el retiro recién creado, ingresar `BOB-014` y usuario `US-P01`: se registra una segunda alerta y el retiro permanece pendiente.
4. Repetir con `BOB-013`: se confirma la recepción; el retiro cambia a **CONFIRMADO** y la bobina a **ENTREGADA**. Esto **no equivale a descontar los metros efectivamente consumidos**.

Si se prefiere trabajar sin navegador:

```bash
python scripts/automatizacion_local.py db/colorink_demo.sqlite BODEGA OP-2026-013 BOB-014 US-B01
python scripts/automatizacion_local.py db/colorink_demo.sqlite BODEGA OP-2026-013 BOB-013 US-B01
python scripts/automatizacion_local.py db/colorink_demo.sqlite PRODUCCION OP-2026-013 BOB-013 US-P01 13
```

El identificador de retiro `13` solo es válido si se parte de la base inicial y se realiza la secuencia indicada sin retiros añadidos anteriormente. En cualquier otro caso utilizar el número indicado por el sistema.

## 6. Consultas, resultados y pruebas

`schema.sql` define relaciones PK/FK, `CHECK`, restricciones `UNIQUE` y disparadores de integridad. `seed.sql` crea 20 tipos de material, 30 bobinas, 15 órdenes, 31 validaciones y 12 retiros de prueba. Las cinco consultas responden a indicadores globales, discrepancias por etapa, retiros pendientes, trazabilidad individual y materiales solicitados con más alertas.

**Resultado de referencia (base sin modificaciones):** 31 escaneos, 10 alertas, 12 retiros, 9 confirmados y 3 pendientes. La tasa de alertas es 10/31 = **32,26 % de escaneos del escenario de prueba**. No es una tasa observada en la empresa.

Para comprobar los mecanismos de bloqueo, ejecutar `python scripts/verificar_entrega.py`. La prueba se realiza en memoria: no modifica la base local ni los CSV. Comprueba cinco consultas, alertas en ambas etapas, validaciones aceptadas, permisos por área, no reutilización de bobinas y que una orden pueda recibir más de una bobina.

## 7. Trazabilidad de la documentación

- `docs/00-caso-pyme.md`: antecedentes tomados de E1 y alcance de E2.
- `docs/01-requerimientos.md`: matriz de diez RF y seis RNF de E1, con cumplimiento total, parcial o no medido.
- `docs/02-bpmn.md`: evolución desde E1 y definición de responsables, desvíos y reglas.
- `docs/03-modelo-datos.md`: entidades, cardinalidades, supuestos, 3FN y diccionario.
- `docs/04-sql-consultas.md`: preguntas de negocio, SQL, lectura de resultados y prueba de reproducción.
- `docs/05-automatizacion-n8n.md`: automatización local equivalente y condiciones necesarias para migrar a n8n.

## 8. Consideraciones para entregar

1. Integrar estas carpetas **en el repositorio de E1**, conservando su evidencia anterior. Revisar las rutas antes de publicar para evitar reemplazos accidentales.
2. Volver a ejecutar `python scripts/verificar_entrega.py` en una copia limpia del repositorio final.
3. Entregar en Aula y `informe/` el **PDF y DOCX del mismo informe**; adjuntar la presentación en Aula y `presentacion/`.
4. Completar `ENLACE_GITHUB.txt` con el **hash o tag real** correspondiente a la versión defendida.
5. Revisar en equipo la declaración de IA y el guion. Los cinco estudiantes deben participar en la defensa.

**Aspectos no probados:** lectores físicos, tiempos de respuesta en operación, usuarios autenticados, lectura de código QR por cámara, conexión al sistema de Colorink, reducción real de errores o ahorros, continuidad operativa y despliegue n8n. No presentarlos como avances logrados.
