-- Q3: Retiros que no han superado el segundo control.
SELECT r.retiro_id,op.codigo AS orden,b.codigo_qr AS bobina,
 u.nombre_mostrado AS responsable_bodega,r.fecha_hora AS fecha_retiro
FROM retiros r JOIN ordenes_produccion op ON op.orden_id=r.orden_id
JOIN bobinas b ON b.bobina_id=r.bobina_id
JOIN usuarios u ON u.usuario_id=r.usuario_bodega_id
WHERE r.estado='PENDIENTE' ORDER BY r.retiro_id;
