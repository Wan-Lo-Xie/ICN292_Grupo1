-- Q4: Orden, material, bobina y responsable, sin datos personales reales.
SELECT op.codigo AS orden,m.codigo AS material,b.codigo_qr AS bobina,
 ub.nombre_mostrado AS responsable_bodega,r.fecha_hora AS retiro,
 r.estado AS estado_retiro, MAX(CASE WHEN v.etapa='PRODUCCION' AND v.resultado='COINCIDE' THEN v.fecha_hora END) AS verificacion_final
FROM retiros r JOIN ordenes_produccion op ON op.orden_id=r.orden_id
JOIN bobinas b ON b.bobina_id=r.bobina_id JOIN materiales m ON m.material_id=b.material_id
JOIN usuarios ub ON ub.usuario_id=r.usuario_bodega_id
LEFT JOIN validaciones v ON v.retiro_id=r.retiro_id
GROUP BY r.retiro_id ORDER BY op.codigo;
