#!/usr/bin/env python3
"""Verificación reproducible sin archivos persistentes ni dependencias externas."""
import pathlib,sqlite3,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from servicio import registrar_lectura,ErrorValidacion
con=sqlite3.connect(':memory:')
con.execute('PRAGMA foreign_keys=ON')
con.executescript((ROOT/'db/schema.sql').read_text(encoding='utf-8'))
con.executescript((ROOT/'db/seed.sql').read_text(encoding='utf-8'))
for consulta in sorted((ROOT/'db/consultas').glob('*.sql')):
    filas=con.execute(consulta.read_text(encoding='utf-8')).fetchall()
    assert filas, consulta
    print('OK consulta',consulta.name,len(filas),'filas')
indicadores=con.execute("SELECT COUNT(*),SUM(resultado='NO_COINCIDE') FROM validaciones").fetchone()
assert indicadores==(31,10),indicadores
assert con.execute("SELECT COUNT(*) FROM retiros WHERE estado='CONFIRMADO'").fetchone()[0]==9
assert con.execute("SELECT COUNT(*) FROM retiros WHERE estado='PENDIENTE'").fetchone()[0]==3
assert con.execute("SELECT COUNT(*) FROM bobinas WHERE estado='ENTREGADA'").fetchone()[0]==9

def debe_fallar(etiqueta,ejecutar):
    try:ejecutar()
    except (sqlite3.IntegrityError,ErrorValidacion):print('OK bloqueo',etiqueta)
    else:raise AssertionError('No se bloqueó: '+etiqueta)

debe_fallar('retiro sin validación',lambda:con.execute("INSERT INTO retiros(orden_id,bobina_id,usuario_bodega_id,validacion_bodega_id,fecha_hora) VALUES(13,13,1,1,'2026-11-21 10:00:00')"))
debe_fallar('resultado falso',lambda:con.execute("INSERT INTO validaciones(orden_id,bobina_id,usuario_id,etapa,resultado,fecha_hora) VALUES(13,14,1,'BODEGA','COINCIDE','2026-11-21 10:00:00')"))
debe_fallar('sin autorización por área',lambda:registrar_lectura(con,'BODEGA','OP-2026-013','BOB-013','US-P01'))
debe_fallar('QR reutilizado',lambda:registrar_lectura(con,'BODEGA','OP-2026-001','BOB-001','US-B01'))
antes=con.execute('SELECT COUNT(*) FROM retiros').fetchone()[0]
mal=registrar_lectura(con,'BODEGA','OP-2026-013','BOB-014','US-B01')
assert mal['resultado']=='NO_COINCIDE'
assert con.execute('SELECT COUNT(*) FROM retiros').fetchone()[0]==antes
print('OK QR incorrecto sin retiro')
bien=registrar_lectura(con,'BODEGA','OP-2026-013','BOB-013','US-B01')
assert bien['resultado']=='COINCIDE'
rid=bien['retiro_id']
assert con.execute('SELECT estado FROM retiros WHERE retiro_id=?',(rid,)).fetchone()[0]=='PENDIENTE'
mal2=registrar_lectura(con,'PRODUCCION','OP-2026-013','BOB-014','US-P01',rid)
assert mal2['resultado']=='NO_COINCIDE'
assert con.execute('SELECT estado FROM retiros WHERE retiro_id=?',(rid,)).fetchone()[0]=='PENDIENTE'
print('OK segunda lectura incorrecta sin confirmar')
bien2=registrar_lectura(con,'PRODUCCION','OP-2026-013','BOB-013','US-P01',rid)
assert bien2['resultado']=='COINCIDE'
assert con.execute('SELECT estado FROM retiros WHERE retiro_id=?',(rid,)).fetchone()[0]=='CONFIRMADO'
assert con.execute('SELECT estado FROM bobinas WHERE bobina_id=13').fetchone()[0]=='ENTREGADA'
print('OK doble lectura + estado entregada')
# Probar que la cardinalidad permite más de una bobina para la misma orden.
con.execute("INSERT INTO bobinas(codigo_qr,material_id,lote,metros_iniciales) VALUES('BOB-EXTRA',13,'LOTE-PRUEBA',500)")
extra=registrar_lectura(con,'BODEGA','OP-2026-013','BOB-EXTRA','US-B01')
assert extra['retiro_id'] != rid
print('OK dos bobinas asociadas a una orden')
print('VERIFICACIÓN COMPLETA: casos positivos, negativos, consultas y cardinalidad')
