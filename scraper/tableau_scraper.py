#!/usr/bin/env python3
"""
Scraper para el dashboard de Tableau Public de Desercion UNAL Sede Bogota.

Estrategia: interceptar respuestas VizQL en Playwright (headless).
Maneja el patron isDeferredBootstrap de Tableau moderno.

Uso:
    python tableau_scraper.py
"""

import asyncio
import json
import csv
import re
import sys
import io
from pathlib import Path
from typing import Any
from playwright.async_api import async_playwright, Response, Page

# UTF-8 en stdout para Windows (evita UnicodeEncodeError con cp1252)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

WORKBOOK = "Desercion_17109576990810"
VIEW = "general_total"

VIZ_URL = (
    f"https://public.tableau.com/views/{WORKBOOK}/{VIEW}"
    "?:embed=y&:showVizHome=no&:toolbar=yes&:animate_transition=no"
)

OUTPUT_DIR = Path(__file__).parent / "data"


# ---------------------------------------------------------------------------
# Parsing de respuestas Tableau
# ---------------------------------------------------------------------------

def _try_json(text: str) -> dict | None:
    """Parsea un fragmento de texto como JSON. Devuelve None si falla."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None


def _raw_decode_first(text: str) -> dict | None:
    """
    Usa raw_decode para extraer el primer objeto JSON valido del texto,
    ignorando cualquier contenido posterior (otros chunks Tableau).
    """
    decoder = json.JSONDecoder()
    text = text.lstrip()
    try:
        obj, _ = decoder.raw_decode(text)
        return obj if isinstance(obj, dict) else None
    except (json.JSONDecodeError, ValueError):
        return None


def parse_tableau_response(raw: str) -> list[dict]:
    """
    Tableau puede enviar multiples objetos JSON concatenados con prefijos de tamano:
        <N>;<JSON1>\\n<M>;<JSON2>\\n...

    Devuelve todos los objetos JSON encontrados (puede haber varios).
    """
    results: list[dict] = []

    # Intento 1: JSON limpio
    r = _try_json(raw)
    if r is not None:
        results.append(r)
        return results

    # Intento 2: usar raw_decode desde la primera '{'
    idx = raw.find('{')
    if idx != -1:
        r = _raw_decode_first(raw[idx:])
        if r is not None:
            results.append(r)
            # Intentar parsear mas objetos desde donde termino el primero
            rest = raw[idx:]
            decoder = json.JSONDecoder()
            pos = 0
            while pos < len(rest):
                rest_strip = rest[pos:].lstrip()
                if not rest_strip:
                    break
                try:
                    obj, end = decoder.raw_decode(rest_strip)
                    if isinstance(obj, dict) and obj not in results:
                        results.append(obj)
                    pos += (len(rest[pos:]) - len(rest_strip)) + end
                except (json.JSONDecodeError, ValueError):
                    # Saltar hasta la siguiente '{'
                    next_brace = rest_strip.find('{', 1)
                    if next_brace == -1:
                        break
                    pos += (len(rest[pos:]) - len(rest_strip)) + next_brace
            return results

    # Intento 3: split por prefijos numericos "N;"
    segments = re.split(r'\d+;', raw)
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        r = _raw_decode_first(seg)
        if r is not None:
            results.append(r)

    return results


def find_best_bootstrap(objects: list[dict]) -> dict | None:
    """
    De todos los JSON capturados, devuelve el que tiene los datos reales
    (secondaryInfo / worldUpdate / presModelMap).
    Prioriza el que tenga dataDictionary con datos.
    """
    scored: list[tuple[int, dict]] = []
    for obj in objects:
        score = 0
        dumped = json.dumps(obj)
        if "secondaryInfo" in dumped:
            score += 100
        if "dataDictionary" in dumped:
            score += 50
        if "dataValues" in dumped:
            score += 50
        if "paneColumnsData" in dumped:
            score += 30
        if "worldUpdate" in dumped:
            score += 20
        if "presModelMap" in dumped:
            score += 10
        scored.append((score, obj))

    scored.sort(key=lambda x: x[0], reverse=True)
    if scored and scored[0][0] > 0:
        print(f"  [score] mejor bootstrap score={scored[0][0]}, claves={list(scored[0][1].keys())[:6]}")
        return scored[0][1]
    return None


# ---------------------------------------------------------------------------
# Captura de red
# ---------------------------------------------------------------------------

class TableauCapture:
    def __init__(self):
        self.all_responses: list[dict] = []   # todos los JSON de VizQL
        self.best_bootstrap: dict | None = None
        self.commands: dict[str, Any] = {}
        self.session_id: str | None = None
        self.session_path: str | None = None

    async def handle_response(self, response: Response) -> None:
        url = response.url

        # Solo nos interesan respuestas de Tableau/CloudFront de la API
        is_vizql = "/vizql/" in url
        is_bootstrap = "bootstrapSession" in url
        if not (is_vizql or is_bootstrap):
            return

        # Capturar session ID
        m = re.search(r"/sessions/([^/?]+)", url)
        if m and self.session_id is None:
            self.session_id = m.group(1)
            self.session_path = re.search(
                r"(/vizql/w/[^/]+/v/[^/]+/sessions/[^/?]+)", url
            )
            if self.session_path:
                self.session_path = self.session_path.group(1)
            print(f"  [session] {self.session_id}")

        try:
            text = await response.text()
        except Exception:
            return

        if not text or len(text) < 10:
            return

        tag = "bootstrap" if is_bootstrap else "vizql"
        print(f"  [{tag}] {len(text):>8} bytes  {url.split('?')[0][-80:]}")

        # Parsear
        objects = parse_tableau_response(text)
        if not objects:
            # Guardar crudo para diagnostico
            (OUTPUT_DIR / f"raw_{tag}_{len(text)}.txt").write_text(text[:500_000], encoding="utf-8")
            return

        self.all_responses.extend(objects)

        # Capturar comandos con nombre
        if "/commands/" in url:
            cmd = url.split("/commands/")[-1].split("?")[0].rstrip("/").split("/")[-1]
            for obj in objects:
                self.commands[cmd] = obj
                print(f"  [cmd] {cmd}")

        # Guardar bootstrap crudo para diagnostico
        if is_bootstrap:
            (OUTPUT_DIR / "bootstrap_raw.txt").write_text(text[:200_000], encoding="utf-8")
            for obj in objects:
                if "isDeferredBootstrap" in obj:
                    print(f"  [bootstrap] isDeferredBootstrap={obj.get('isDeferredBootstrap')}")


# ---------------------------------------------------------------------------
# Extraccion de datos
# ---------------------------------------------------------------------------

def extract_rows(pmm: dict, value_index: list) -> list[dict]:
    """Extrae filas de un presModelMap dado su value_index."""
    rows: list[dict] = []

    vd_node = pmm.get("vizData", {})
    # Navegar envoltorios
    if "presModelHolder" in vd_node:
        vd_node = (
            vd_node["presModelHolder"]
            .get("genPresModelMapPresModel", {})
            .get("presModelMap", {})
        )

    for sheet_name, sheet_model in (vd_node.items() if isinstance(vd_node, dict) else []):
        sheet_data = (
            sheet_model.get("presModelHolder", {})
            .get("genVizDataPresModel", {})
        )
        if not sheet_data:
            continue

        columns_data = sheet_data.get("columnsData", {})
        pane_cols = sheet_data.get("paneColumnsData", {})

        col_names = [
            c.get("fieldCaption", c.get("fn", f"col_{i}"))
            for i, c in enumerate(columns_data.get("columns", []))
        ]
        print(f"  [sheet] '{sheet_name}': {len(col_names)} cols")

        for pane in pane_cols.get("paneColumnsList", []):
            col_idx_list = pane.get("vizPaneColumns", [])
            if not col_idx_list:
                continue
            n_rows = len(col_idx_list[0].get("aliasIndices", []))
            for r_i in range(n_rows):
                row: dict = {"_sheet": sheet_name}
                for c_j, col_info in enumerate(col_idx_list):
                    aliases = col_info.get("aliasIndices", [])
                    if r_i < len(aliases):
                        vi = aliases[r_i]
                        real = abs(vi) - 1 if vi < 0 else vi
                        val = value_index[real] if real < len(value_index) else vi
                        col = col_names[c_j] if c_j < len(col_names) else f"col_{c_j}"
                        row[col] = val
                rows.append(row)
    return rows


def extract_data_from_objects(objects: list[dict]) -> list[dict]:
    """
    Intenta multiples rutas de datos en los objetos JSON capturados.
    Devuelve las filas encontradas.
    """
    best = find_best_bootstrap(objects)
    if best is None:
        print("  [-] Ningun objeto con datos reconocibles")
        return []

    # Buscar el presModelMap en distintas rutas
    pmm_candidates = [
        best.get("secondaryInfo", {}).get("presModelMap", {}),
        best.get("worldUpdate", {}).get("presModelMap", {}),
        best.get("world", {}).get("presModelMap", {}),
        best,
    ]

    for pmm in pmm_candidates:
        if not pmm or not isinstance(pmm, dict):
            continue

        # Construir value_index desde dataDictionary
        dd = (
            pmm.get("dataDictionary", {})
            .get("presModelHolder", {})
            .get("genDataDictionaryPresModel", {})
        )
        value_index: list[Any] = []
        for seg in dd.get("dataSegments", {}).values():
            value_index.extend(seg.get("dataValues", []))

        if not value_index:
            continue

        print(f"  [data] value_index: {len(value_index)} entradas")
        rows = extract_rows(pmm, value_index)
        if rows:
            return rows

    return []


# ---------------------------------------------------------------------------
# Guardado
# ---------------------------------------------------------------------------

def save_json(data: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  [+] JSON -> {path.name}")


def save_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [+] CSV -> {path.name} ({len(rows)} filas)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    capture = TableauCapture()

    async with async_playwright() as p:
        print("[*] Lanzando Chromium headless...")
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            locale="es-CO",
        )
        page = await ctx.new_page()
        page.on("response", capture.handle_response)

        print(f"[*] Cargando: {VIZ_URL}")
        try:
            await page.goto(VIZ_URL, wait_until="domcontentloaded", timeout=60_000)
        except Exception as e:
            print(f"  [-] Nav error: {e}")

        print("[*] Esperando render completo...")
        try:
            await page.wait_for_selector(".tabCanvas, #tabBootstrap, iframe", timeout=40_000)
        except Exception:
            pass

        # Esperar las respuestas asincronas del deferred bootstrap
        await asyncio.sleep(8)

        print(f"[*] Responses capturadas: {len(capture.all_responses)}")
        await browser.close()

    # ---------------------------------------------------------------------------
    print("\n[*] Procesando...")

    if not capture.all_responses:
        print("[!] Sin datos capturados. Revisa bootstrap_raw.txt")
        sys.exit(1)

    # Guardar todos los objetos para diagnostico
    save_json(capture.all_responses, OUTPUT_DIR / "all_responses.json")

    rows = extract_data_from_objects(capture.all_responses)

    if rows:
        save_csv(rows, OUTPUT_DIR / f"{VIEW}_datos.csv")
        save_json(rows, OUTPUT_DIR / f"{VIEW}_datos.json")
        print(f"\n[OK] {len(rows)} filas extraidas.")
    else:
        print("\n[!] No se pudieron extraer filas estructuradas.")
        print("    Ejecuta: python explorar_bootstrap.py data/all_responses.json")
        # Guardar el mejor candidato
        best = find_best_bootstrap(capture.all_responses)
        if best:
            save_json(best, OUTPUT_DIR / "best_candidate.json")

    if capture.commands:
        save_json(capture.commands, OUTPUT_DIR / "commands.json")

    print(f"\n[*] Archivos en: {OUTPUT_DIR}/")

    # Invocar el extractor si hay commands.json
    if capture.commands:
        print("\n[*] Ejecutando extractor de datos...")
        import subprocess
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "extraer_datos.py")],
            capture_output=True, text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)


if __name__ == "__main__":
    asyncio.run(main())
