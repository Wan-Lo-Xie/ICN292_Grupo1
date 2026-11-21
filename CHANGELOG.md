# Historial de cambios de la solución

## Entrega 2 · 21 de noviembre de 2026

Se mantiene el caso Colorink y la dificultad operacional identificada en E1: discrepancias entre bobina retirada y material requerido por la orden. El trabajo no modifica la actividad de impresión propiamente tal.

**Proceso:** revisión del TO-BE para distinguir lectura en bodega, bloqueo, retiro pendiente, lectura en producción y confirmación. Se definieron las excepciones y su correspondencia con los registros de datos.

**Datos:** modelo de siete entidades en 3FN, con claves primarias, foráneas, unicidad y restricciones. Se admite más de una bobina por orden, sin permitir reutilizar una misma bobina en varios retiros. Se diferencia la condición «entregada a producción» del consumo de material.

**SQL y verificación:** construcción de esquema SQLite, carga sintética, cinco consultas y pruebas automatizadas, incluidos casos negativos y comprobación de integridad referencial.

**Automatización:** servicio transaccional en Python, utilidad de consola e interfaz web local para demostrar el flujo. No se ha implementado ni desplegado un flujo n8n real.

**Documentación:** informe Word/PDF, diagramas, archivos Markdown, resultados CSV, presentación y guion de defensa. Se explicitaron limitaciones para evitar confundir la simulación con indicadores reales de Colorink.

## Entrega 1 · septiembre de 2026

Diagnóstico y propuesta inicial registrados en el informe «Propuesta SIG para una PYME»: caso Colorink, entrevista, requerimientos RF/RNF y modelos AS-IS y TO-BE preliminares. Documento fuente proporcionado por el equipo.
