# Identificación de la PYME
Para comprender a cabalidad la empresa con la que se trabajará (Colorink), es fundamental entender el contexto en el que se mueve dicha organización y las circunstancias en las que fue creada. Esta empresa surge como respuesta a problemáticas que enfrentaban los clientes de una empresa previa llamada ATC (RUT 76.076.930-4).

Cronológicamente, se nos menciona que ATC fue creada en 2004 por Jaime Vásquez, su actual jefe y dueño, con el propósito de brindar soluciones de automatización de sistemas relacionados con el flujo de caja, movimientos de inventario, entre otros procesos. Para la gestión de inventarios se utilizaban etiquetas con códigos de barras específicos que permitían registrar los productos dentro de los sistemas implementados. Sin embargo, muchos clientes no contaban con este sistema de etiquetado, lo que generaba una importante dificultad: ¿de dónde obtener las etiquetas necesarias para registrar los productos dentro del nuevo software adquirido?

Como respuesta a esta necesidad, en 2007 surge Colorink, también fundada por Jaime Vásquez. Esta empresa se dedica a la flexografía y comenzó inicialmente como una solución para los clientes de ATC. Con el tiempo, evolucionó hasta convertirse en una empresa independiente que comercializa etiquetas para diversas organizaciones. Entre sus clientes más destacados se encuentran Adidas Chile, Aquachile y Tommy Hilfiger Chile, entre otros.

Colorink (RUT 76.404.254-9), ubicada en Avenida Santa Rosa 4470, comuna de San Joaquín, pertenece al rubro de la importación, comercialización y producción flexográfica. Cuenta con aproximadamente 10 trabajadores, distribuidos principalmente en tres áreas: producción, comercial y administrativa.

Cabe mencionar que, si bien es una empresa consolidada con más de diez años de trayectoria, sigue siendo considerada una pyme. Por esta razón, muchos de sus trabajadores desempeñan funciones para ambas empresas, tanto para ATC como para Colorink, especialmente en las áreas comercial y administrativa. Esto se debe a que ambas organizaciones operan en conjunto y comparten las mismas instalaciones. Sin embargo, para efectos de este trabajo, el enfoque estará puesto exclusivamente en el área flexográfica de Colorink, dejando de lado las operaciones de ATC.

# Evidencia de Existencia

**Acta de Entrevista**

Fecha y hora de la entrevista: 1 de septiembre, 11:00 horas.

Entrevistados y cargos: Jaime Vásquez, fundador de Colorink; Roberto Castro, jefe de bodega.

Entrevistadores: Antonia Flores, Bastián Guajardo, Wan Lo Xie, Carolina Tavil y Mateo Vásquez.

Asunto:
Se realizó una entrevista al fundador y al jefe de bodega de la empresa Colorink con el objetivo de comprender y analizar el proceso de creación de etiquetas, identificando oportunidades de mejora dentro de sus operaciones.

Desarrollo de la entrevista:
La entrevista comenzó con una breve introducción realizada por Jaime Vásquez, fundador de Colorink, quien explicó los orígenes de la empresa y describió su estructura organizacional actual.

Posteriormente, se abordó el proceso de creación de etiquetas, identificándose que una de las principales problemáticas se encuentra en la etapa inicial del proceso, específicamente en el traspaso de materiales desde la bodega hacia el área de manufactura.

Más adelante, se incorporó a la entrevista Roberto Castro, jefe de bodega, quien profundizó en las actividades relacionadas con la manufactura y confirmó que el traspaso de materiales desde la bodega al área de producción constituye el principal problema operativo del proceso, debido a las dificultades de control y trazabilidad que se generan en esta etapa.

# Problema de Negocio

Al momento de existir una alta carga de trabajo, se generan discrepancias entre el material solicitado por el cliente y el material retirado desde la bodega para su producción. Este constituye uno de los principales problemas dentro del proceso, ya que genera impactos tanto en los tiempos como en los costos de producción.

Lo anterior ocurre debido a que, cuando se utiliza un material incorrecto, es necesario repetir parcial o totalmente el proceso productivo. Considerando una producción promedio de 100.000 etiquetas, el tiempo estimado de fabricación es de aproximadamente 20 horas. Bajo un escenario pesimista, asumiendo que el error es detectado una vez finalizado el proceso de impresión, el tiempo total de producción podría duplicarse respecto de lo inicialmente planificado.

Como consecuencia, se produciría un aumento significativo en los tiempos de entrega y en los costos asociados a la producción, debido al consumo adicional de materiales, horas de trabajo y uso de maquinaria. El desglose de estos impactos se presenta a continuación:

https://github.com/Wan-Lo-Xie/ICN292_Grupo1/blob/45c1dc46e53dc9a27bbed760ed2779ab11098b12/assets/ICN292_P100_E1_Flores_Guajardo_Tavil_Vasquez_Xie(costos%20operarios).jpg

Se consideran 2 tipos de operarios, esto debido a que, dependiendo de la producción que se realizará, se necesitan distintos tipos de operarios. Esto se debe principalmente al hecho de que existen producciones que llevan materiales y pinturas más complejas de trabajar, lo que hace que solo el operario de tipo 1 pueda llevar a cabo dicha producción. Por lo que, si se continúa con este análisis, los costos estipulados para la impresión de inmediato aumentan en un 50%. Además de esto, se debe considerar la materia prima que se pierde en este proceso, la cual entraría a ser considerada como merma.

Además, es fundamental que, si el proceso de impresión se retrasa, retrasa todo el proceso en sí, esto debido a que es una cadena la cual inicia con la impresión, pero a la que le siguen procesos como el troquelado y el rebobinado, por lo que el despacho se retrasa también.

Es por esto por lo que hemos decidido atacar este problema, puesto que, si bien no es uno que ocurra con demasiada frecuencia, es lo suficientemente importante, a tal punto que puede llegar a retrasar el despacho en días si no se detecta a tiempo.

# Objetivo del SIG Propuesto

Se integrará un sistema que mediante una doble verificación utilizando inteligencia artificial que logre verificar que el material retirado de la bodega es el indicado en la orden de producción.
