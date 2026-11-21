# 01. Requerimientos y evidencia de cumplimiento

Los códigos RF y RNF se mantienen en la numeración de E1. «Demostrado» significa probado en los datos y scripts de laboratorio, **no desplegado en la operación real de Colorink**. «Parcial» identifica una funcionalidad representada sin resolver todas sus condiciones de uso.

| ID | Requerimiento establecido en E1 | Evidencia de E2 | Estado |
|---|---|---|---|
| RF-01 | Identificar a quien retira material | `usuarios` y relación con `retiros` | Demostrado en laboratorio |
| RF-02 | Consultar la orden de producción | `ordenes_produccion` y selector web | Demostrado |
| RF-03 | Asociar un QR a cada bobina | `bobinas.codigo_qr` y catálogo de prueba | Demostrado con identificadores sintéticos |
| RF-04 | Permitir escanear el QR | Campo compatible con lector tipo teclado, sin cámara | Parcial |
| RF-05 | Comparar material con orden | Servicio de validación y trigger SQL | Demostrado |
| RF-06 | Generar alerta y bloquear retiro incompatible | Validación `NO_COINCIDE`, ausencia de retiro | Demostrado |
| RF-07 | Registrar usuario, fecha, orden y bobina | `validaciones` y `retiros` | Demostrado |
| RF-08 | Segunda lectura antes de imprimir | Etapa `PRODUCCION`, confirmación condicionada | Demostrado |
| RF-09 | Historial de validaciones y retiros | Consulta 04 y resultados CSV | Demostrado |
| RF-10 | Indicadores simples de alertas y retiros | Consultas 01, 02 y 05; interfaz local | Demostrado con seed |
| RNF-01 | Interfaz sencilla | Página web de laboratorio en localhost | Parcial: sin usuarios reales |
| RNF-02 | Responder en pocos segundos | Sin prueba de tiempos ni carga | No evaluado |
| RNF-03 | Evitar retiros con datos faltantes | FK, NOT NULL, CHECK y disparadores | Demostrado |
| RNF-04 | Acceso solo a usuarios autorizados | Restricción por área; sin inicio de sesión | Parcial |
| RNF-05 | Ejecutar el prototipo localmente | Python y SQLite en localhost | Demostrado |
| RNF-06 | Registrar datos necesarios | Identificadores, áreas, eventos y estados | Demostrado en demo |

## Reglas de aceptación

**A1.** Ante un QR cuyo material difiere del exigido, el sistema registra la alerta, pero no crea un retiro.

**A2.** Ante un material correcto y bobina disponible, se crea un retiro pendiente; la bobina queda reservada para evitar reutilizaciones.

**A3.** Si producción lee otra bobina o un material incorrecto, el retiro sigue pendiente.

**A4.** Si producción verifica el mismo QR de un retiro pendiente y el material coincide, la entrega se confirma. El sistema no presume que el material haya sido consumido en la máquina.

**A5.** Una persona cuyo área no corresponde a la tarea no puede registrar una validación a través de la lógica del sistema.

Estos criterios se comprueban con `python scripts/verificar_entrega.py`. Los requisitos de autenticación real, cámara y conexión con los sistemas existentes quedan pendientes de evaluación de campo.
