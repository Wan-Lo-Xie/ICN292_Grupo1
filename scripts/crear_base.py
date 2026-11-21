#!/usr/bin/env python3
"""Crea una base nueva de demostración. No sobrescribe una base existente."""
import sqlite3, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
out=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'db'/'colorink_demo.sqlite'
if out.exists():raise SystemExit(f'Ya existe {out}. Muévala o indique otra ruta.')
out.parent.mkdir(parents=True,exist_ok=True)
with sqlite3.connect(out) as conn:
 conn.execute('PRAGMA foreign_keys=ON')
 conn.executescript((ROOT/'db'/'schema.sql').read_text(encoding='utf-8'))
 conn.executescript((ROOT/'db'/'seed.sql').read_text(encoding='utf-8'))
 print('Base creada:',out,'| validaciones:',conn.execute('SELECT COUNT(*) FROM validaciones').fetchone()[0])
