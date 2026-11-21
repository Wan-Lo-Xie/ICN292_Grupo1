#!/usr/bin/env python3
"""Servidor de demostración local Colorink. No exponer a Internet ni usar con datos reales."""
from __future__ import annotations
import json, sqlite3, sys, pathlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from servicio import registrar_lectura,ErrorValidacion
DB=ROOT/'db'/'colorink_demo.sqlite'
STATIC={'/':'index.html','/estilos.css':'estilos.css','/interfaz.js':'interfaz.js'}
TYPES={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8'}

def db():
    conn=sqlite3.connect(DB,timeout=5)
    conn.row_factory=sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    return conn
class Controlador(BaseHTTPRequestHandler):
    def respuesta(self,data,codigo=200):
        raw=json.dumps(data,ensure_ascii=False,default=str).encode('utf-8')
        self.send_response(codigo);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(raw)))
        self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        if self.path in STATIC:
            file=p=pathlib.Path(__file__).parent/STATIC[self.path]
            raw=file.read_bytes()
            self.send_response(200);self.send_header('Content-Type',TYPES[file.suffix])
            self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw);return
        if self.path!='/api/estado':return self.respuesta({'error':'Recurso no encontrado'},404)
        with db() as c:
            def lista(sql):return [dict(r) for r in c.execute(sql)]
            self.respuesta({'ordenes':lista("SELECT codigo, material_requerido_id FROM ordenes_produccion ORDER BY codigo"),
             'usuarios':lista("SELECT codigo, area FROM usuarios WHERE activo=1 ORDER BY codigo"),
             'pendientes':lista("SELECT r.retiro_id, o.codigo AS orden, b.codigo_qr AS bobina FROM retiros r JOIN ordenes_produccion o ON o.orden_id=r.orden_id JOIN bobinas b ON b.bobina_id=r.bobina_id WHERE r.estado='PENDIENTE' ORDER BY r.retiro_id"),
             'indicadores':dict(c.execute("SELECT COUNT(*) AS escaneos, COALESCE(SUM(resultado='NO_COINCIDE'),0) AS alertas FROM validaciones").fetchone()),
             'total_retiros':c.execute('SELECT COUNT(*) FROM retiros').fetchone()[0],
             'confirmados':c.execute("SELECT COUNT(*) FROM retiros WHERE estado='CONFIRMADO'").fetchone()[0]})
    def do_POST(self):
        if self.path!='/api/validar':return self.respuesta({'error':'Recurso no encontrado'},404)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<=0 or size>8192:return self.respuesta({'error':'Solicitud demasiado grande o vacía'},400)
            data=json.loads(self.rfile.read(size))
            with db() as c:
                obj=registrar_lectura(c,str(data.get('etapa','')),str(data.get('orden','')),
                       str(data.get('qr','')),str(data.get('usuario','')),
                       int(data['retiro_id']) if data.get('retiro_id') else None)
            self.respuesta(obj)
        except (ValueError,TypeError,ErrorValidacion,json.JSONDecodeError) as e:
            self.respuesta({'error':str(e)},400)
        except sqlite3.Error:
            self.respuesta({'error':'No se pudo completar la operación en la base local.'},500)
    def log_message(self,format,*args):pass
if __name__=='__main__':
    if not DB.is_file():raise SystemExit('Primero ejecute: python scripts/crear_base.py')
    puerto=int(sys.argv[1]) if len(sys.argv)>1 else 8765
    print(f'Colorink · Prototipo académico disponible en http://127.0.0.1:{puerto}')
    print('Para finalizar, presione Ctrl+C. No exponer este servidor a Internet.')
    ThreadingHTTPServer(('127.0.0.1',puerto),Controlador).serve_forever()
