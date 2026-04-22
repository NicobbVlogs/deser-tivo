#!/usr/bin/env python3
"""
Herramienta de diagnóstico para explorar la estructura del bootstrap JSON
capturado por tableau_scraper.py.

Uso:
    python explorar_bootstrap.py [ruta_al_json]

Si no se pasa ruta, busca data/general_total_bootstrap.json por defecto.
"""

import json
import sys
from pathlib import Path


def mostrar_arbol(obj: object, prefijo: str = "", max_depth: int = 6, depth: int = 0) -> None:
    """Imprime la estructura de un dict/list de forma compacta."""
    if depth > max_depth:
        print(f"{prefijo}... (profundidad máxima)")
        return

    if isinstance(obj, dict):
        for k, v in list(obj.items())[:30]:  # máx 30 claves por nivel
            tipo = type(v).__name__
            if isinstance(v, (dict, list)):
                n = len(v)
                print(f"{prefijo}{k}:  [{tipo}, {n} items]")
                mostrar_arbol(v, prefijo + "  ", max_depth, depth + 1)
            else:
                val_str = repr(v)[:80]
                print(f"{prefijo}{k}: {val_str}")
        if len(obj) > 30:
            print(f"{prefijo}... ({len(obj) - 30} claves más)")

    elif isinstance(obj, list):
        for i, item in enumerate(obj[:5]):  # máx 5 items de lista
            tipo = type(item).__name__
            if isinstance(item, (dict, list)):
                print(f"{prefijo}[{i}]: [{tipo}]")
                mostrar_arbol(item, prefijo + "  ", max_depth, depth + 1)
            else:
                print(f"{prefijo}[{i}]: {repr(item)[:80]}")
        if len(obj) > 5:
            print(f"{prefijo}... ({len(obj) - 5} items más)")


def buscar_listas_grandes(obj: object, path: str = "", min_size: int = 10) -> None:
    """Encuentra listas/dicts grandes que probablemente sean datos."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            nuevo_path = f"{path}.{k}"
            if isinstance(v, list) and len(v) >= min_size:
                print(f"  Lista en {nuevo_path}: {len(v)} items, tipo={type(v[0]).__name__ if v else '?'}")
            buscar_listas_grandes(v, nuevo_path, min_size)
    elif isinstance(obj, list):
        for i, item in enumerate(obj[:3]):
            buscar_listas_grandes(item, f"{path}[{i}]", min_size)


def main() -> None:
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
    else:
        json_path = Path(__file__).parent / "data" / "general_total_bootstrap.json"

    if not json_path.exists():
        print(f"[!] Archivo no encontrado: {json_path}")
        print("    Ejecuta primero tableau_scraper.py")
        sys.exit(1)

    print(f"[*] Cargando {json_path} ({json_path.stat().st_size // 1024} KB)...\n")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 60)
    print("ESTRUCTURA GENERAL (primeras claves)")
    print("=" * 60)
    mostrar_arbol(data, max_depth=4)

    print("\n" + "=" * 60)
    print("LISTAS GRANDES (probables datos reales, ≥10 items)")
    print("=" * 60)
    buscar_listas_grandes(data)

    # Buscar específicamente la ruta canónica
    print("\n" + "=" * 60)
    print("RUTAS CLAVE DE TABLEAU")
    print("=" * 60)
    rutas = [
        ("secondaryInfo.presModelMap", lambda d: d.get("secondaryInfo", {}).get("presModelMap", {})),
        ("world.presModelMap", lambda d: d.get("world", {}).get("presModelMap", {})),
        ("worldUpdate.presModelMap", lambda d: d.get("worldUpdate", {}).get("presModelMap", {})),
    ]
    for nombre, getter in rutas:
        try:
            sub = getter(data)
            if sub:
                claves = list(sub.keys())
                print(f"\n  {nombre}: {claves}")
        except Exception:
            pass


if __name__ == "__main__":
    main()
