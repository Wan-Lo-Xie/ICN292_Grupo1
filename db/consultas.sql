-- 01_kpi_generales.sql
-- Q1: Indicadores del período completo de demostración (por escaneo).
SELECT COUNT(*) AS escaneos, SUM(resultado='NO_COINCIDE') AS alertas,
 ROUND(100.0*SUM(resultado='NO_COINCIDE')/COUNT(*),2) AS porcentaje_alertas,
 (SELECT COUNT(*) FROM retiros) AS retiros_registrados,
 (SELECT COUNT(*) FROM retiros WHERE estado='CONFIRMADO') AS retiros_confirmados
FROM validaciones;

-- 02_alertas_etapa.sql
-- Q2: Dónde se concentra el riesgo operacional.
SELECT etapa, COUNT(*) AS escaneos,
 SUM(resultado='NO_COINCIDE') AS alertas,
 ROUND(100.0*SUM(resultado='NO_COINCIDE')/COUNT(*),2) AS porcentaje_alertas
FROM validaciones GROUP BY etapa ORDER BY etapa;

-- 03_retiros_pendientes.sql
-- Q3: Retiros que no han superado el segundo control.
SELECT r.retiro_id,op.codigo AS orden,b.codigo_qr AS bobina,
 u.nombre_mostrado AS responsable_bodega,r.fecha_hora AS fecha_retiro
FROM retiros r JOIN ordenes_produccion op ON op.orden_id=r.orden_id
JOIN bobinas b ON b.bobina_id=r.bobina_id
JOIN usuarios u ON u.usuario_id=r.usuario_bodega_id
WHERE r.estado='PENDIENTE' ORDER BY r.retiro_id;

-- 04_trazabilidad.sql
-- Q4: Orden, material, bobina y responsable, sin datos personales reales.
SELECT op.codigo AS orden,m.codigo AS material,b.codigo_qr AS bobina,
 ub.nombre_mostrado AS responsable_bodega,r.fecha_hora AS retiro,
 r.estado AS estado_retiro, MAX(CASE WHEN v.etapa='PRODUCCION' AND v.resultado='COINCIDE' THEN v.fecha_hora END) AS verificacion_final
FROM retiros r JOIN ordenes_produccion op ON op.orden_id=r.orden_id
JOIN bobinas b ON b.bobina_id=r.bobina_id JOIN materiales m ON m.material_id=b.material_id
JOIN usuarios ub ON ub.usuario_id=r.usuario_bodega_id
LEFT JOIN validaciones v ON v.retiro_id=r.retiro_id
GROUP BY r.retiro_id ORDER BY op.codigo;

-- 05_materiales_alertados.sql
-- Q5: Material solicitado con más diferencias en el escaneo.
SELECT m.codigo AS material_solicitado,COUNT(*) AS alertas
FROM validaciones v JOIN ordenes_produccion op ON op.orden_id=v.orden_id
JOIN materiales m ON m.material_id=op.material_requerido_id
WHERE v.resultado='NO_COINCIDE'
GROUP BY m.material_id ORDER BY alertas DESC,m.codigo;
