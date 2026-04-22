#!/usr/bin/env python3
"""
Genera src/lib/modelo.ts a partir de datos_desercion.json.

Modelo: regresión logística con coeficientes derivados de tasas observadas.
Para cada variable X y categoría c:
  coef[X][c] = log( tasa(X=c) / tasa_base )

Predicción:
  log_odds = logit(tasa_base) + sum(coef[Xi][ci])
  riesgo   = sigmoid(log_odds)
"""

import json
import math
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "src" / "lib" / "datos_desercion.json"
OUT_FILE = ROOT / "src" / "lib" / "modelo.ts"

with open(DATA_FILE, encoding="utf-8") as f:
    d = json.load(f)

# ── Tasa base ──────────────────────────────────────────────────────────────
tasa_base: float = d["kpi_tasa_desercion"][0]["AGR(Tasa deserción)"]

# ── Helper ─────────────────────────────────────────────────────────────────
def tasas_categoricas(tabla: str, col_cat: str, col_des: str = "SUMA(Desertores)",
                      col_mat: str = "AGR(Matriculados)", min_n: int = 100) -> dict[str, float]:
    rows = [
        r for r in d.get(tabla, [])
        if r.get("Nombres de medidas", "Desertores") == "Desertores"
    ]
    result: dict[str, float] = {}
    for r in rows:
        cat = str(r.get(col_cat, "")).strip()
        des = r.get(col_des) or 0
        mat = r.get(col_mat) or 0
        if not cat or int(mat) < min_n:
            continue
        result[cat] = int(des) / int(mat)
    return result

# ── Tablas de tasas ────────────────────────────────────────────────────────
programas  = tasas_categoricas("por_programa_curricular", "PROGRAMA_CURRICULAR", min_n=150)
estratos   = tasas_categoricas("por_estrato", "ESTRATO", min_n=50)
colegios   = {
    k: v for k, v in
    tasas_categoricas("por_tipo_colegio", "TIPCOLEGIO", min_n=200).items()
    if k != "Sin información"   # artefacto de datos
}
generos    = tasas_categoricas("por_genero", "GENERO", min_n=10)
niv_mat    = tasas_categoricas("por_nivelacion_matematicas", "NIVELA_MATEMATICAS", min_n=50)
niv_lecto  = tasas_categoricas("por_nivelacion_lectoescritura", "NIVELA_LECTOESCRITURA", min_n=50)

# ── Coeficientes log(ratio) ────────────────────────────────────────────────
def coefs(tasas: dict[str, float]) -> dict[str, float]:
    return {k: math.log(v / tasa_base) for k, v in tasas.items() if v > 0}

coefs_programa  = coefs(programas)
coefs_estrato   = coefs(estratos)
coefs_colegio   = coefs(colegios)
coefs_genero    = coefs(generos)
coefs_niv_mat   = coefs(niv_mat)
coefs_niv_lecto = coefs(niv_lecto)

# ── Generar TypeScript ─────────────────────────────────────────────────────
def ts_record(d: dict[str, float], indent: int = 4) -> str:
    pad = " " * indent
    lines = [f'{pad}"{k}": {v:.8f},' for k, v in sorted(d.items())]
    return "{\n" + "\n".join(lines) + "\n" + " " * (indent - 2) + "}"

ts = f'''\
// Generado automaticamente por scraper/generar_modelo.py
// Modelo de riesgo de desercion — datos reales UNAL Sede Bogota (2025-2)
//
// Metodo: modelo multiplicativo de riesgo (log-lineal / Naive Bayes multinomial).
// Para cada variable X con categorias c_i:
//   coeficiente[c_i] = log( tasa_observada(c_i) / tasa_base )
// Prediccion final:
//   log_odds = logit(tasa_base) + sum(coef_Xi)
//   riesgo   = sigmoid(log_odds)
//
// Interpretacion: cada coeficiente representa cuanto aumenta o disminuye
// el log-odds de desercion respecto al promedio global (tasa_base = {tasa_base:.4f}).
// Coef > 0 => mayor riesgo; Coef < 0 => menor riesgo.

export const TASA_BASE = {tasa_base};

// Coeficientes por variable (log risk ratio respecto a tasa_base)
export const COEFS = {{
  programa: {ts_record(coefs_programa)},

  estrato: {ts_record(coefs_estrato)},

  tipo_colegio: {ts_record(coefs_colegio)},

  genero: {ts_record(coefs_genero)},

  nivelacion_matematicas: {ts_record(coefs_niv_mat)},

  nivelacion_lectoescritura: {ts_record(coefs_niv_lecto)},
}} satisfies Record<string, Record<string, number>>;

// Opciones validas para cada campo (para los <select> en la UI)
export const OPCIONES = {{
  programa: {json.dumps(sorted(programas.keys()), ensure_ascii=False, indent=2)},
  estrato: {json.dumps(sorted(estratos.keys(), key=lambda x: int(x) if x.isdigit() else x), ensure_ascii=False)},
  tipo_colegio: {json.dumps(sorted(colegios.keys()), ensure_ascii=False)},
  genero: {json.dumps(list(generos.keys()), ensure_ascii=False)},
  nivelacion_matematicas: ["NO", "SI"],
  nivelacion_lectoescritura: ["NO", "SI"],
}} as const;

export type PerfilEstudiante = {{
  programa: string;
  estrato: string;
  tipo_colegio: string;
  genero: string;
  nivelacion_matematicas: "NO" | "SI";
  nivelacion_lectoescritura: "NO" | "SI";
}};

function logit(p: number): number {{
  return Math.log(p / (1 - p));
}}

function sigmoid(x: number): number {{
  return 1 / (1 + Math.exp(-x));
}}

/**
 * Estima la probabilidad de desercion para un perfil de estudiante.
 * Devuelve un numero en [0, 1].
 *
 * Si una variable no esta en la tabla de coeficientes, se ignora
 * (equivale a asumir riesgo promedio para esa dimension).
 */
export function predecir(perfil: PerfilEstudiante): number {{
  let logOdds = logit(TASA_BASE);

  const vars: [keyof typeof COEFS, string][] = [
    ["programa",                perfil.programa],
    ["estrato",                 perfil.estrato],
    ["tipo_colegio",            perfil.tipo_colegio],
    ["genero",                  perfil.genero],
    ["nivelacion_matematicas",  perfil.nivelacion_matematicas],
    ["nivelacion_lectoescritura", perfil.nivelacion_lectoescritura],
  ];

  for (const [dim, valor] of vars) {{
    const coef = COEFS[dim][valor];
    if (coef !== undefined) logOdds += coef;
  }}

  return sigmoid(logOdds);
}}
'''

OUT_FILE.write_text(ts, encoding="utf-8")
print(f"[OK] {OUT_FILE}")
print(f"     Tasa base: {tasa_base:.4f} ({tasa_base*100:.2f}%)")
print(f"     Programas: {len(coefs_programa)}")
print(f"     Estratos:  {len(coefs_estrato)}")
