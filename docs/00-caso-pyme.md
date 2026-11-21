# 00. Caso de estudio: Colorink

## Antecedentes del levantamiento

El caso corresponde a Colorink, empresa dedicada a fabricar etiquetas mediante flexografía. Según el informe de la Entrega 1, fue fundada en 2007 y cuenta con aproximadamente diez trabajadores. Comparte instalaciones y algunas funciones administrativas con ATC; la investigación, sin embargo, se limita al proceso de Colorink. Los antecedentes de funcionamiento utilizados aquí provienen de la entrevista del 1 de septiembre, consignada por el equipo en E1, con Jaime Vásquez y Roberto Castro.

En la secuencia levantada, la orden especifica el material requerido y precede a la impresión, el troquelado, el rebobinado y el despacho. Una bobina mal seleccionada en bodega puede ser recibida sin una comprobación independiente. El error se traslada entonces al proceso productivo, donde su corrección puede exigir merma y reproceso.

El informe E1 menciona una producción de referencia de 100.000 etiquetas en aproximadamente 20 horas. Plantea, como escenario desfavorable, otras 20 horas de impresión si se detecta el material equivocado cuando la tirada ya terminó. Ese valor es una **estimación de riesgo presentada en E1**, no una estadística obtenida mediante la solución de E2.

## Pregunta de diseño

¿Cómo dejar constancia de que la bobina retirada de bodega corresponde a una orden concreta y asegurar que producción reciba esa misma bobina antes de iniciar la impresión?

La solución se acota a dos controles de material mediante un identificador QR, asociado a una bobina específica, y a un registro de eventos. Se mantienen fuera del estudio las ventas, la facturación y el funcionamiento de las máquinas de impresión.

## Continuidad E1 → E2

| Aspecto | Entrega 1 | Entrega 2 |
|---|---|---|
| Caso | Colorink, área flexográfica | Se conserva el mismo caso |
| Problema | Discrepancias en retiro de materia prima | Se precisan controles y excepciones |
| Solución | Doble lectura QR propuesta | Modelo de eventos, reglas SQL y aplicación local demostrativa |
| BPMN | AS-IS y TO-BE preliminares | TO-BE formalizado y tareas asociadas a datos |
| Datos | Necesidad de registrar materiales y responsables | Esquema relacional 3FN, diccionario y restricciones |
| Resultado | Beneficios esperados | Pruebas reproducibles **sin métricas reales** |

El proyecto no introduce otro problema de negocio: desarrolla técnicamente lo propuesto en E1 y hace explícitos sus límites de implementación.

**Fuente primaria:** *Propuesta SIG para una PYME: Colorink*, Entrega 1, P100, segundo semestre 2026 (archivo aportado por el equipo, pp. 3–12 y anexos).
