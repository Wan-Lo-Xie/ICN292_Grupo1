# 04. Implementación SQL y consultas de negocio

## 1. Entorno y modo de ejecución

El motor escogido es **SQLite 3**, por su facilidad de reproducción local. `db/schema.sql` crea tablas, claves, índices, restricciones y triggers. `db/seed.sql` carga un conjunto ficticio de prueba: 3 proveedores, 20 materiales, 5 usuarios, 30 bobinas, 15 órdenes, 31 validaciones y 12 retiros. Para ejecutar y comprobar los datos:

```bash
python scripts/verificar_entrega.py
python scripts/crear_base.py
python scripts/ejecutar_consultas.py
python scripts/exportar_resultados.py
```

Los CSV de `evidencias/` se originan en consultas ejecutadas y se regeneran con `exportar_resultados.py`. No se rellenan a mano.

## 2. Consultas y sentido empresarial

| Archivo SQL | Pregunta de gestión | Salida en la base original de prueba |
|---|---|---|
| `01_kpi_generales.sql` | ¿Cuántos intentos de escaneo se hicieron y cuántos presentaron discrepancias? | 31 intentos; 10 alertas; 32,26 %; 12 retiros; 9 confirmados |
| `02_alertas_etapa.sql` | ¿En qué punto se detectan las diferencias? | Bodega: 7 alertas de 19 lecturas. Producción: 3 de 12. |
| `03_retiros_pendientes.sql` | ¿Qué bobinas requieren segunda verificación? | 3 retiros pendientes: OP-2026-010, -011 y -012 |
| `04_trazabilidad.sql` | ¿Qué material salió, quién lo retiró y qué ocurrió luego? | 12 retiros con orden, QR, responsable, fecha y confirmación |
| `05_materiales_alertados.sql` | ¿Qué materiales solicitados estuvieron asociados a intentos incompatibles? | 10 alertas agrupadas por material requerido |

**Cuidado con el denominador.** La tasa de alertas es *número de escaneos no coincidentes / número total de escaneos*. No corresponde dividir por el total de retiros: los intentos incompatibles se bloquean y, justamente por esa razón, no todos producen una fila en `retiros`. El indicador describe **intentos de lectura**, no pedidos erróneos ni producción desperdiciada.

## 3. Interpretación de resultados

Que existan diez alertas demuestra que el conjunto de pruebas contiene situaciones de discrepancia y que las consultas pueden contabilizarlas. No significa que Colorink tenga una tasa de error del 32,26 %. Los resultados de `02_alertas_etapa.sql` muestran cómo distinguir el lugar de detección. El listado de pendientes de la consulta 03 es útil para seguimiento diario; la consulta 04 permitiría una auditoría de responsabilidades, siempre que los registros provinieran de una operación real.

Tampoco se utilizan las estimaciones de 20 horas de E1 para informar horas «ahorradas»: no se realizaron observaciones de campo ni se levantó una línea base de antes y después.

## 4. Controles más allá de la consulta

`tr_validacion_integridad` exige coherencia material–orden y un usuario habilitado para la etapa. `tr_retiro_integridad` exige una validación correcta de bodega y disponibilidad de la bobina. `tr_reservar_bobina` marca la bobina como reservada. `tr_confirmar_retiro` confirma la entrega tras la segunda lectura. `tr_proteger_confirmacion` rechaza una confirmación sin evidencia de recepción conforme.

El código Python utiliza SQL parametrizado. Los bloqueos más relevantes se ensayan en `verificar_entrega.py` y las transacciones se pueden repetir desde la interfaz de localhost sobre una copia de la base de prueba.

## 5. Limitaciones del indicador

Una alerta puede repetirse para una misma orden y varias lecturas pueden corresponder a un solo retiro. Para un futuro piloto se recomienda distinguir intentos, órdenes afectadas, bobinas efectivamente entregadas de forma incorrecta y horas de reproceso. Solo así podrían calcularse diferencias operativas sin confundir escenarios sintéticos con desempeño empresarial.
