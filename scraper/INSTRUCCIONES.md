# Scraper - Desercion UNAL Tableau Public

## Instalacion (una sola vez)

```bash
cd scraper
uv venv .venv
uv pip install -r requirements.txt
.venv/Scripts/playwright install chromium   # Windows
# o: .venv/bin/playwright install chromium  # Linux/Mac
```

## Ejecutar todo el pipeline

```bash
.venv/Scripts/python tableau_scraper.py
```

El scraper hace dos cosas automaticamente:
1. Abre el dashboard en Chromium headless e intercepta la API VizQL
2. Llama a `extraer_datos.py` para parsear y exportar las tablas

## Archivos de salida

```
scraper/data/
  commands.json              <- respuesta cruda del render
  desercion_unal.json        <- JSON consolidado con todas las tablas (168 KB)
  tablas/
    serie_temporal_absolutos.csv    <- desertores y matriculados por periodo (2015-2025)
    serie_temporal_tasas.csv        <- tasa de desercion por periodo
    por_facultad.csv                <- 16 facultades
    por_programa_curricular.csv     <- 50 programas
    por_estrato.csv                 <- estratos 1-6
    por_genero.csv                  <- por genero
    por_departamento_procedencia.csv
    distribucion_pbm.csv            <- distribucion del PBM
    distribucion_edad.csv
    clasificacion_papa.csv          <- 371 clasificaciones por PAPA
    ... y mas
```

## Si solo quieres re-extraer (sin volver a scrapear)

```bash
.venv/Scripts/python extraer_datos.py
```

## Integracion con SvelteKit

El JSON consolidado se copia automaticamente:

```bash
cp data/desercion_unal.json ../src/lib/datos_desercion.json
```

En el componente Svelte:

```svelte
<script>
  import datos from '$lib/datos_desercion.json'
  // datos.serie_temporal_absolutos, datos.por_facultad, etc.
</script>
```

## Estructura del dashboard (zonas con datos)

| Tabla | Zona | Filas | Descripcion |
|---|---|---|---|
| serie_temporal_absolutos | 29 | 44 | Desertores y desvinculados por periodo |
| serie_temporal_tasas | 35 | 44 | Tasas porcentuales por periodo |
| por_facultad | 67 | 32 | Por facultad |
| por_programa_curricular | 68 | 100 | Por programa (50 progs x 2 metricas) |
| clasificacion_papa | 69 | 371 | Clasificacion de desercion vs PAPA |
| distribucion_pbm | 109 | 93 | Histograma del PBM |
| por_estrato | 107 | 12 | Por estrato socioeconomico |
| mapa_departamentos | 162 | 33 | Con coordenadas lat/lon |
