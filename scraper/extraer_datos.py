#!/usr/bin/env python3
"""
Extrae los datos de desercion desde el JSON capturado por tableau_scraper.py.

Uso:
    python extraer_datos.py

Requiere que exista data/commands.json (generado por tableau_scraper.py).
"""

import json
import csv
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

DATA_DIR = Path(__file__).parent / "data"


# ---------------------------------------------------------------------------
# Lookup de valores por tipo de dato
# ---------------------------------------------------------------------------

def build_type_lookup(data_cols: list) -> dict:
    """
    Construye un mapa dtype -> lista de valores.
    Tableau almacena enteros, reales y strings en columnas separadas.
    """
    lookup = {}
    if len(data_cols) >= 1:
        vals = data_cols[0]["dataValues"]
        lookup["integer"] = vals
        lookup["long"] = vals
    if len(data_cols) >= 2:
        vals = data_cols[1]["dataValues"]
        lookup["real"] = vals
        lookup["float"] = vals
    if len(data_cols) >= 3:
        vals = data_cols[2]["dataValues"]
        lookup["cstring"] = vals
        lookup["string"] = vals
    return lookup


def resolve_value(lookup: dict, dtype: str, idx: int):
    """Resuelve un indice a su valor real. Indice negativo = None."""
    if idx is None or idx < 0:
        return None
    col = lookup.get(dtype)
    if col is None:
        return idx
    return col[idx] if idx < len(col) else None


# ---------------------------------------------------------------------------
# Extraccion de una zona
# ---------------------------------------------------------------------------

def extract_zone(zone_id: str, zone: dict, lookup: dict) -> list[dict]:
    """Extrae todas las filas de una zona del dashboard."""
    vd = zone.get("presModelHolder", {}).get("visual", {}).get("vizData", {})
    pcd = vd.get("paneColumnsData", {})
    vdcols = pcd.get("vizDataColumns", [])
    panes = pcd.get("paneColumnsList", [])

    if not vdcols or not panes:
        return []

    # Columnas con datos utiles (descartamos tuple_id que no tiene fieldCaption)
    data_col_metas = [c for c in vdcols if c.get("fieldCaption") and c.get("dataType") in lookup]

    rows: list[dict] = []

    for pane_i, pane in enumerate(panes):
        vpc_list = pane.get("vizPaneColumns", [])

        # Determinar numero de filas del pane
        n_rows = 0
        for vpc in vpc_list:
            ai = vpc.get("aliasIndices", [])
            ti = vpc.get("tupleIds", [])
            n_rows = max(n_rows, len(ai), len(ti))

        if n_rows == 0:
            continue

        for row_i in range(n_rows):
            row: dict = {"_zone": zone_id}

            for col_meta in data_col_metas:
                caption = col_meta["fieldCaption"]
                dtype = col_meta["dataType"]
                col_indices = col_meta.get("columnIndices", [])

                # columnIndices tiene un valor por pane; si hay menos que panes, repetir el primero
                vpc_idx = (
                    col_indices[pane_i]
                    if pane_i < len(col_indices)
                    else (col_indices[0] if col_indices else None)
                )
                if vpc_idx is None or vpc_idx >= len(vpc_list):
                    continue

                vpc = vpc_list[vpc_idx]
                ai = vpc.get("aliasIndices", [])
                if row_i < len(ai):
                    row[caption] = resolve_value(lookup, dtype, ai[row_i])

            if len(row) > 1:  # mas de solo _zone
                rows.append(row)

    return rows


# ---------------------------------------------------------------------------
# Nombres descriptivos para las zonas
# ---------------------------------------------------------------------------

ZONE_NAMES = {
    "3":   "kpi_total",
    "22":  "kpi_matriculados",
    "23":  "kpi_tasa_desercion",
    "24":  "kpi_desertores",
    "25":  "kpi_tasa_desvinculacion",
    "27":  "kpi_desvinculados",
    "29":  "serie_temporal_absolutos",
    "35":  "serie_temporal_tasas",
    "59":  "por_subacceso_grupo",
    "60":  "por_nivelacion_matematicas",
    "61":  "por_nivelacion_lectoescritura",
    "62":  "por_nivel_ingles",
    "67":  "por_facultad",
    "68":  "por_programa_curricular",
    "69":  "clasificacion_papa",
    "104": "por_genero",
    "105": "por_departamento_procedencia",
    "106": "por_tipo_colegio",
    "107": "por_estrato",
    "108": "kpi_pbm_promedio",
    "109": "distribucion_pbm",
    "110": "kpi_edad_promedio",
    "111": "distribucion_edad",
    "162": "mapa_departamentos",
    "180": "por_subacceso",
    "393": "matriculas_por_periodo",
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    commands_path = DATA_DIR / "commands.json"
    if not commands_path.exists():
        print(f"[!] No encontrado: {commands_path}")
        print("    Ejecuta primero: python tableau_scraper.py")
        sys.exit(1)

    print(f"[*] Cargando {commands_path.name}...")
    with open(commands_path, encoding="utf-8") as f:
        cmds = json.load(f)

    cmd = cmds.get("notify-first-client-render-occurred", {})
    apm = (
        cmd.get("vqlCmdResponse", {})
        .get("layoutStatus", {})
        .get("applicationPresModel", {})
    )
    if not apm:
        print("[!] No se encontro applicationPresModel en commands.json")
        sys.exit(1)

    # Construir lookup de valores
    data_cols = (
        apm.get("dataDictionary", {})
        .get("dataSegments", {})
        .get("0", {})
        .get("dataColumns", [])
    )
    if not data_cols:
        print("[!] dataDictionary vacio")
        sys.exit(1)

    lookup = build_type_lookup(data_cols)
    print(f"[*] Lookup: {len(lookup)} tipos, "
          f"enteros={len(lookup.get('integer',[]))}, "
          f"reales={len(lookup.get('real',[]))}, "
          f"strings={len(lookup.get('cstring',[]))}")

    zones = (
        apm.get("workbookPresModel", {})
        .get("dashboardPresModel", {})
        .get("zones", {})
    )
    print(f"[*] Zonas encontradas: {len(zones)}")

    all_tables: dict[str, list[dict]] = {}
    total_rows = 0

    for zone_id in sorted(zones.keys(), key=lambda x: int(x)):
        rows = extract_zone(zone_id, zones[zone_id], lookup)
        if not rows:
            continue
        name = ZONE_NAMES.get(zone_id, f"zona_{zone_id}")
        all_tables[name] = rows
        total_rows += len(rows)
        print(f"  [+] {name:45s} {len(rows):4d} filas")

    print(f"\n[*] Total: {total_rows} filas en {len(all_tables)} tablas")

    # Guardar cada tabla como CSV y JSON separado
    tables_dir = DATA_DIR / "tablas"
    tables_dir.mkdir(parents=True, exist_ok=True)

    for name, rows in all_tables.items():
        # CSV
        csv_path = tables_dir / f"{name}.csv"
        fieldnames = list(rows[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    # JSON consolidado con todas las tablas
    master_path = DATA_DIR / "desercion_unal.json"
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(all_tables, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Tablas individuales en: {tables_dir}/")
    print(f"[OK] JSON consolidado:       {master_path}")


if __name__ == "__main__":
    main()
