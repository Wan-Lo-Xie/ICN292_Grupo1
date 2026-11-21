-- Q2: Dónde se concentra el riesgo operacional.
SELECT etapa, COUNT(*) AS escaneos,
 SUM(resultado='NO_COINCIDE') AS alertas,
 ROUND(100.0*SUM(resultado='NO_COINCIDE')/COUNT(*),2) AS porcentaje_alertas
FROM validaciones GROUP BY etapa ORDER BY etapa;
