#!/usr/bin/env python3
"""Interfaz de consola para las validaciones de bodega y producción.
Uso: python scripts/automatizacion_local.py db/colorink_demo.sqlite BODEGA OP-2026-013 BOB-014 US-B01
Uso: python scripts/automatizacion_local.py db/colorink_demo.sqlite PRODUCCION OP-2026-013 BOB-013 US-P01 13
"""
from pathlib import Path
import sqlite3,sys
from servicio import registrar_lectura, ErrorValidacion
if __name__ == "__main__":
    if len(sys.argv) not in (6,7):
        raise SystemExit("Uso: python scripts/automatizacion_local.py BASE ETAPA ORDEN QR USUARIO [RETIRO_ID]")
    ruta,etapa,orden,qr,usuario = sys.argv[1:6]
    if not Path(ruta).is_file():raise SystemExit("Primero cree la base con: python scripts/crear_base.py")
    try:
        with sqlite3.connect(ruta) as con:
            con.execute("PRAGMA foreign_keys = ON")
            obj = registrar_lectura(con,etapa,orden,qr,usuario,int(sys.argv[6]) if len(sys.argv)==7 else None)
        print("Resultado:",obj['resultado'],"| Validación:",obj['validacion_id'],"| Retiro:",obj['retiro_id'])
        print(obj['mensaje'])
    except (ErrorValidacion,ValueError) as ex:
        raise SystemExit("OPERACIÓN RECHAZADA: "+str(ex))
