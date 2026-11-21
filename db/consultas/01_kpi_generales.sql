-- Q1: Indicadores del período completo de demostración (por escaneo).
SELECT COUNT(*) AS escaneos, SUM(resultado='NO_COINCIDE') AS alertas,
 ROUND(100.0*SUM(resultado='NO_COINCIDE')/COUNT(*),2) AS porcentaje_alertas,
 (SELECT COUNT(*) FROM retiros) AS retiros_registrados,
 (SELECT COUNT(*) FROM retiros WHERE estado='CONFIRMADO') AS retiros_confirmados
FROM validaciones;
