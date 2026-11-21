# Guion de defensa — Colorink / ICN-292 E2

**Duración prevista: 6 minutos y 40 segundos, con ocho diapositivas.** Esta distribución reserva un margen de seguridad frente al máximo de siete minutos. Los cinco integrantes intervienen. Antes de presentarla, cada participante debe reformular el texto en sus propias palabras y practicar el cambio de turno.

| Diapositiva | Responsable propuesto | Tiempo | Idea a explicar |
|---|---|---:|---|
| 1. Portada | Antonia Flores | 0:20 | Empresa, tema y objetivo de la E2 |
| 2. Problema | Antonia Flores | 0:50 | Qué se observó en E1 y por qué importa |
| 3. Proceso TO-BE | Bastián Guajardo | 0:55 | Primer y segundo control; alertas y decisiones |
| 4. Datos 3FN | Wan Lo Xie | 0:55 | Identificadores, entidades y separación entre objetos y eventos |
| 5. Consultas | Mateo Vásquez | 0:55 | Qué consultamos y por qué el seed no mide la empresa |
| 6. Automatización | Carolina Tavil | 1:15 | Reglas y demostración local de un QR incorrecto y uno correcto |
| 7. Resultados y límites | Mateo Vásquez | 0:50 | Qué se probó y qué falta validar |
| 8. Cierre | Bastián Guajardo | 0:40 | Valor de la trazabilidad y próximos pasos |
| **Total** | **Cinco integrantes** | **6:40** | |

## Relato sugerido (no memorizar palabra por palabra)

**1. Antonia:** «En el trabajo anterior identificamos un punto de control débil en Colorink, empresa dedicada a las etiquetas flexográficas. La propuesta de esta entrega es verificar que la bobina que sale de bodega sea la que realmente corresponde a la orden, y comprobarla nuevamente antes de imprimir».

**2. Antonia:** «Según la entrevista que documentamos en la primera entrega, el problema aparece al transferir material desde bodega a producción. Si la bobina es incorrecta, el error puede descubrirse tarde. La referencia de 20 horas es un escenario expuesto en E1: no es un ahorro que hayamos medido».

**3. Bastián:** «Agregamos dos decisiones. La primera ocurre al intentar retirar la bobina: si el material no coincide, queda una alerta y no hay retiro. Si coincide, el sistema registra un retiro pendiente. La segunda ocurre al recibirla: solo al verificar el mismo QR se confirma que la bobina fue entregada».

**4. Wan Lo:** «Distribuimos la información en siete tablas para no repetir nombres y atributos en los movimientos. Una bobina se relaciona con un material, una orden indica qué material exige y cada lectura queda asociada a usuario, fecha y resultado. Esto permite conservar las discrepancias sin fabricar retiros que no fueron autorizados».

**5. Mateo:** «Construimos cinco consultas: indicadores, alertas por etapa, pendientes, trazabilidad y materiales asociados a alertas. El conjunto sintético produce 31 lecturas y 10 alertas, pero esos números solo verifican que las consultas y las reglas funcionan. No representan estadísticas reales de Colorink».

**6. Carolina:** «La automatización se hizo con Python y SQLite, que funcionan en localhost sin servicios externos. La entrada contiene orden, QR y responsable. Al ingresar un QR incompatible, la base registra una alerta y rechaza el retiro. Con el correcto, genera una operación pendiente; la segunda lectura permite confirmarla. No existe un flujo n8n instalado ni una conexión al sistema de la empresa». Si el tiempo lo permite, mostrar **solo el primer rechazo y el retiro correcto**, sin realizar toda la secuencia en vivo.

**7. Mateo:** «Conseguimos un modelo normalizado, un proceso coherente y SQL que impide inconsistencias. La siguiente etapa exige probar el sistema con lectores y personas reales, integrar inventario, medir tiempos y resolver usuarios y devoluciones».

**8. Bastián:** «El aporte no es solo el código: la decisión de bodega queda conectada con registros y evidencia para auditarla. Presentamos una solución técnica reproducible y sus límites, que sirve como base para una validación posterior en Colorink».

## Preguntas probables del docente

- **¿Por qué SQLite?** Por reproducibilidad en un entorno limpio; cumple la demostración SQL, aunque una integración real requeriría revisar el motor utilizado por Colorink.
- **¿Dónde está n8n?** La pauta admite una herramienta homóloga. El flujo implementado es un servicio local Python/SQLite; el equivalente conceptual con n8n está documentado en docs/05-automatizacion-n8n.md.
- **¿Qué prueba la tasa del 32,26 %?** Que 10 de las 31 lecturas del escenario sintético son discrepantes. No indica tasa real de errores ni ahorro.
- **¿Qué evita reutilizar una bobina?** Su unicidad en retiros, la verificación de disponibilidad y el cambio de estado; las transacciones evitan confirmar un retiro no validado.
- **¿Por qué el sistema no usa inteligencia artificial?** El requisito de correspondencia es verificable por identificadores y reglas SQL. No se implementó reconocimiento de imagen ni un modelo entrenado; se descartó afirmar una capacidad no demostrada.
- **¿Qué falta?** Autenticación real, lectores físicos, integración con inventario, devoluciones/consumos parciales, manejo de concurrencia y medición de desempeño en la empresa.
