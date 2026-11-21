#!/usr/bin/env python3
"""Reproduce los CSV de evidencia directamente desde schema.sql y seed.sql."""
import csv
import sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'evidencias'
out.mkdir(exist_ok=True)
c=sqlite3.connect(':memory:')
c.execute('PRAGMA foreign_keys=ON')
c.executescript((ROOT/'db'/'schema.sql').read_text(encoding='utf-8'))
c.executescript((ROOT/'db'/'seed.sql').read_text(encoding='utf-8'))
for f in sorted((ROOT/'db'/'consultas').glob('*.sql')):
 cur=c.execute(f.read_text(encoding='utf-8'))
 names=[d[0] for d in cur.description]
 with (out/(f.stem+'.csv')).open('w',encoding='utf-8-sig',newline='') as handle:
  writer=csv.writer(handle)
  writer.writerow(names)
  writer.writerows(cur.fetchall())
 print('CSV reproducido:',f.stem+'.csv')
c.close()
