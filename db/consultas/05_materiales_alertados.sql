-- Q5: Material solicitado con más diferencias en el escaneo.
SELECT m.codigo AS material_solicitado,COUNT(*) AS alertas
FROM validaciones v JOIN ordenes_produccion op ON op.orden_id=v.orden_id
JOIN materiales m ON m.material_id=op.material_requerido_id
WHERE v.resultado='NO_COINCIDE'
GROUP BY m.material_id ORDER BY alertas DESC,m.codigo;
