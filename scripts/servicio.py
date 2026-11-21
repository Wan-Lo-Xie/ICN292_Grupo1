"""Reglas transaccionales para la demostración académica de Colorink.
El lector QR se emula ingresando el identificador visible de una bobina.
No utiliza el sistema operativo real de la empresa ni realiza autenticación.
"""
from __future__ import annotations
import datetime as dt
import sqlite3

class ErrorValidacion(ValueError):
    pass

def registrar_lectura(con: sqlite3.Connection, etapa: str, orden: str, codigo_qr: str,
                      usuario: str, retiro_id: int | None = None) -> dict:
    if etapa not in ("BODEGA", "PRODUCCION"):
        raise ErrorValidacion("La etapa debe ser BODEGA o PRODUCCION.")
    if (etapa == "PRODUCCION") != (retiro_id is not None):
        raise ErrorValidacion("Solo la lectura de producción requiere el número del retiro.")
    orden_row = con.execute("SELECT orden_id, material_requerido_id FROM ordenes_produccion WHERE codigo=?",(orden,)).fetchone()
    bobina_row = con.execute("SELECT bobina_id, material_id FROM bobinas WHERE codigo_qr=?",(codigo_qr,)).fetchone()
    usuario_row = con.execute("SELECT usuario_id FROM usuarios WHERE codigo=?",(usuario,)).fetchone()
    if not orden_row:
        raise ErrorValidacion("La orden indicada no existe.")
    if not bobina_row:
        raise ErrorValidacion("El identificador QR indicado no existe.")
    if not usuario_row:
        raise ErrorValidacion("El usuario no existe.")
    if etapa == "BODEGA":
        estado_bobina=con.execute("SELECT estado FROM bobinas WHERE bobina_id=?",(bobina_row[0],)).fetchone()[0]
        # El escaneo de una bobina ocupada se registra, pero jamás se crea otro retiro.
        disponible=(estado_bobina == "DISPONIBLE")
    else:
        row=con.execute("SELECT orden_id,bobina_id,estado FROM retiros WHERE retiro_id=?",(retiro_id,)).fetchone()
        if not row or row[0] != orden_row[0] or row[2] != "PENDIENTE":
            raise ErrorValidacion("El retiro no existe, no está pendiente o pertenece a otra orden.")
        disponible=(row[1] == bobina_row[0])
    coincide=(orden_row[1] == bobina_row[1]) and disponible
    # En BODEGA, un QR de material correcto pero ya reservado es una alerta de disponibilidad.
    # La restricción SQL calcula la coincidencia de material; se clasifica el escaneo no disponible
    # con resultado COINCIDE, pero la creación de retiro se rechaza y revierte la transacción.
    if etapa == "BODEGA" and orden_row[1] == bobina_row[1] and not disponible:
        raise ErrorValidacion("La bobina ya fue reservada o entregada; no se permite un segundo retiro.")
    resultado = "COINCIDE" if coincide else "NO_COINCIDE"
    fecha = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with con:
            v = con.execute("""INSERT INTO validaciones(orden_id,bobina_id,usuario_id,retiro_id,etapa,resultado,fecha_hora,observacion)
                VALUES(?,?,?,?,?,?,?,?)""",(orden_row[0],bobina_row[0],usuario_row[0],retiro_id,etapa,resultado,fecha,
                "Lectura realizada en demostración local"))
            creado=None
            if etapa == "BODEGA" and coincide:
                c=con.execute("""INSERT INTO retiros(orden_id,bobina_id,usuario_bodega_id,validacion_bodega_id,fecha_hora)
                    VALUES(?,?,?,?,?)""",(orden_row[0],bobina_row[0],usuario_row[0],v.lastrowid,fecha))
                creado=c.lastrowid
            if etapa == "PRODUCCION" and coincide:
                ok=con.execute("SELECT estado FROM retiros WHERE retiro_id=?",(retiro_id,)).fetchone()
                if not ok or ok[0] != "CONFIRMADO":
                    raise ErrorValidacion("La confirmación no quedó registrada.")
        return dict(etapa=etapa,orden=orden,qr=codigo_qr,usuario=usuario,resultado=resultado,
                    validacion_id=v.lastrowid,retiro_id=creado or retiro_id,
                    mensaje=("Coincidencia en bodega. Retiro pendiente de segunda validación." if etapa=="BODEGA" and coincide else
                       "Segunda lectura conforme. Entrega a producción confirmada." if coincide else
                       "ALERTA: QR incompatible; operación bloqueada hasta corregirlo."))
    except sqlite3.IntegrityError as ex:
        raise ErrorValidacion("La base de datos rechazó el intento: "+str(ex)) from ex
