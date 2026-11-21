#!/usr/bin/env python3
"""Ejecuta las cinco consultas SQL y muestra resultados verificables."""
import sqlite3, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
path=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'db'/'colorink_demo.sqlite'
if not path.is_file():raise SystemExit('Cree primero la base con: python scripts/crear_base.py')
with sqlite3.connect(f'file:{path}?mode=ro',uri=True) as con:
 for script in sorted((ROOT/'db'/'consultas').glob('*.sql')):
  cur=con.execute(script.read_text(encoding='utf-8')); headers=[x[0] for x in cur.description]
  print('\n###',script.name, '\n | '.join(headers))
  for row in cur.fetchall():print(' | '.join('—' if x is None else str(x) for x in row))
