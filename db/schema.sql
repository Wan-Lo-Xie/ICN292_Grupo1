-- ICN292 E2 / Colorink. Motor: SQLite >= 3.35; SQL reproducible.
-- DEMOSTRACIÓN ACADÉMICA: no es la base real de Colorink.
PRAGMA foreign_keys = ON;

CREATE TABLE proveedores (
 proveedor_id INTEGER PRIMARY KEY,
 nombre TEXT NOT NULL UNIQUE
);
CREATE TABLE materiales (
 material_id INTEGER PRIMARY KEY,
 codigo TEXT NOT NULL UNIQUE,
 familia TEXT NOT NULL,
 acabado TEXT NOT NULL,
 ancho_mm INTEGER NOT NULL CHECK(ancho_mm > 0),
 proveedor_id INTEGER NOT NULL REFERENCES proveedores(proveedor_id) ON DELETE RESTRICT,
 activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN(0,1)),
 UNIQUE(familia,acabado,ancho_mm,proveedor_id)
);
CREATE TABLE usuarios (
 usuario_id INTEGER PRIMARY KEY,
 codigo TEXT NOT NULL UNIQUE,
 nombre_mostrado TEXT NOT NULL,
 area TEXT NOT NULL CHECK(area IN('BODEGA','PRODUCCION','ADMINISTRACION')),
 activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN(0,1))
);
CREATE TABLE bobinas (
 bobina_id INTEGER PRIMARY KEY,
 codigo_qr TEXT NOT NULL UNIQUE,
 material_id INTEGER NOT NULL REFERENCES materiales(material_id) ON DELETE RESTRICT,
 lote TEXT NOT NULL,
 metros_iniciales INTEGER NOT NULL CHECK(metros_iniciales > 0),
 estado TEXT NOT NULL DEFAULT 'DISPONIBLE' CHECK(estado IN('DISPONIBLE','RESERVADA','ENTREGADA'))
);
CREATE TABLE ordenes_produccion (
 orden_id INTEGER PRIMARY KEY,
 codigo TEXT NOT NULL UNIQUE,
 cliente_ref TEXT NOT NULL,
 material_requerido_id INTEGER NOT NULL REFERENCES materiales(material_id) ON DELETE RESTRICT,
 cantidad_etiquetas INTEGER NOT NULL CHECK(cantidad_etiquetas > 0),
 fecha_creacion TEXT NOT NULL,
 estado TEXT NOT NULL CHECK(estado IN('PROGRAMADA','EN_PROCESO','FINALIZADA'))
);
CREATE TABLE validaciones (
 validacion_id INTEGER PRIMARY KEY,
 orden_id INTEGER NOT NULL REFERENCES ordenes_produccion(orden_id) ON DELETE RESTRICT,
 bobina_id INTEGER NOT NULL REFERENCES bobinas(bobina_id) ON DELETE RESTRICT,
 usuario_id INTEGER NOT NULL REFERENCES usuarios(usuario_id) ON DELETE RESTRICT,
 retiro_id INTEGER REFERENCES retiros(retiro_id) ON DELETE RESTRICT,
 etapa TEXT NOT NULL CHECK(etapa IN('BODEGA','PRODUCCION')),
 resultado TEXT NOT NULL CHECK(resultado IN('COINCIDE','NO_COINCIDE')),
 fecha_hora TEXT NOT NULL,
 observacion TEXT NOT NULL DEFAULT '',
 CHECK((etapa='BODEGA' AND retiro_id IS NULL) OR (etapa='PRODUCCION' AND retiro_id IS NOT NULL))
);
CREATE TABLE retiros (
 retiro_id INTEGER PRIMARY KEY,
 orden_id INTEGER NOT NULL REFERENCES ordenes_produccion(orden_id) ON DELETE RESTRICT,
 bobina_id INTEGER NOT NULL REFERENCES bobinas(bobina_id) ON DELETE RESTRICT,
 usuario_bodega_id INTEGER NOT NULL REFERENCES usuarios(usuario_id) ON DELETE RESTRICT,
 validacion_bodega_id INTEGER NOT NULL UNIQUE REFERENCES validaciones(validacion_id) ON DELETE RESTRICT,
 fecha_hora TEXT NOT NULL,
 estado TEXT NOT NULL DEFAULT 'PENDIENTE' CHECK(estado IN('PENDIENTE','CONFIRMADO')),
 UNIQUE(bobina_id)
);
CREATE INDEX idx_validaciones_fecha ON validaciones(fecha_hora);
CREATE INDEX idx_validaciones_etapa_resultado ON validaciones(etapa,resultado);
CREATE INDEX idx_bobinas_material ON bobinas(material_id);
CREATE INDEX idx_retiros_estado ON retiros(estado);

-- Un escaneo jamás puede declarar que coincide si la BD encuentra otra cosa.
CREATE TRIGGER tr_validacion_integridad BEFORE INSERT ON validaciones
BEGIN
 SELECT CASE WHEN NOT EXISTS (SELECT 1 FROM usuarios u WHERE u.usuario_id=NEW.usuario_id AND u.activo=1 AND (u.area=NEW.etapa OR u.area='ADMINISTRACION'))
   THEN RAISE(ABORT,'Usuario no autorizado para la etapa') END;
 SELECT CASE WHEN NEW.etapa='PRODUCCION' AND NOT EXISTS (
    SELECT 1 FROM retiros r WHERE r.retiro_id=NEW.retiro_id AND r.orden_id=NEW.orden_id AND r.estado='PENDIENTE'
 ) THEN RAISE(ABORT,'El retiro no existe o no esta pendiente') END;
 SELECT CASE WHEN NEW.resultado <> (
  CASE WHEN EXISTS(
    SELECT 1 FROM bobinas b JOIN ordenes_produccion op ON op.orden_id=NEW.orden_id
    WHERE b.bobina_id=NEW.bobina_id AND b.material_id=op.material_requerido_id
      AND (NEW.etapa='BODEGA' OR EXISTS(SELECT 1 FROM retiros r WHERE r.retiro_id=NEW.retiro_id AND r.bobina_id=NEW.bobina_id))
  ) THEN 'COINCIDE' ELSE 'NO_COINCIDE' END
 ) THEN RAISE(ABORT,'Resultado incongruente con la orden, bobina o retiro') END;
END;

-- Solo se crea retiro si hubo validación de bodega correcta y la bobina está disponible.
CREATE TRIGGER tr_retiro_integridad BEFORE INSERT ON retiros
BEGIN
 SELECT CASE WHEN NOT EXISTS (
  SELECT 1 FROM validaciones v JOIN bobinas b ON b.bobina_id=v.bobina_id
  WHERE v.validacion_id=NEW.validacion_bodega_id AND v.etapa='BODEGA'
    AND v.resultado='COINCIDE' AND v.orden_id=NEW.orden_id
    AND v.bobina_id=NEW.bobina_id AND v.usuario_id=NEW.usuario_bodega_id
    AND b.estado='DISPONIBLE'
 ) THEN RAISE(ABORT,'Retiro requiere escaneo correcto y bobina disponible') END;
 SELECT CASE WHEN NEW.estado<>'PENDIENTE' THEN RAISE(ABORT,'Retiro debe iniciar pendiente') END;
END;
CREATE TRIGGER tr_reservar_bobina AFTER INSERT ON retiros
BEGIN
 UPDATE bobinas SET estado='RESERVADA' WHERE bobina_id=NEW.bobina_id;
END;
-- La segunda lectura autoriza la entrega a producción; no acredita consumo en impresión.
-- Una orden puede incluir distintas bobinas, pero cada bobina solo se entrega una vez.
CREATE TRIGGER tr_confirmar_retiro AFTER INSERT ON validaciones
WHEN NEW.etapa='PRODUCCION' AND NEW.resultado='COINCIDE'
BEGIN
 UPDATE retiros SET estado='CONFIRMADO' WHERE retiro_id=NEW.retiro_id AND estado='PENDIENTE';
 UPDATE bobinas SET estado='ENTREGADA' WHERE bobina_id=NEW.bobina_id AND estado='RESERVADA';
END;
CREATE TRIGGER tr_proteger_confirmacion BEFORE UPDATE OF estado ON retiros
WHEN NEW.estado='CONFIRMADO'
BEGIN
 SELECT CASE WHEN NOT EXISTS (
   SELECT 1 FROM validaciones v WHERE v.retiro_id=NEW.retiro_id
    AND v.etapa='PRODUCCION' AND v.resultado='COINCIDE' AND v.bobina_id=NEW.bobina_id
 ) THEN RAISE(ABORT,'Falta verificacion de produccion') END;
END;
