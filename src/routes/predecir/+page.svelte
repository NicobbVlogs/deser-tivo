<script lang="ts">
    import Riesgo from "$lib/components/Riesgo.svelte";
    import AlertaTemprana from "$lib/components/AlertaTemprana.svelte";
    import { predecir, OPCIONES, type PerfilEstudiante } from "$lib/modelo";
    import { fade } from "svelte/transition";

    let perfil = $state<PerfilEstudiante>({
        programa: "",
        estrato: "",
        tipo_colegio: "",
        genero: "",
        nivelacion_matematicas: "NO",
        nivelacion_lectoescritura: "NO",
    });

    const completo = $derived(
        !!perfil.programa && !!perfil.estrato && !!perfil.tipo_colegio && !!perfil.genero
    );

    const riesgo = $derived(completo ? predecir(perfil) : null);
    const esAlto = $derived(riesgo !== null && riesgo > 0.09);
</script>

<div transition:fade={{ duration: 150 }} id="container">
    <p class="intro">
        Selecciona el perfil del estudiante para estimar su riesgo de deserción.
        El modelo usa datos reales de UNAL Sede Bogotá (periodo 2025&#8209;2).
    </p>

    <h2>Perfil Primario del estudiante</h2>

    <form class="tarjeta">
        <div class="question">
            <label for="sel-programa">Programa curricular</label>
            <select id="sel-programa" bind:value={perfil.programa}>
                <option value="" disabled>Seleccionar…</option>
                {#each OPCIONES.programa as p}
                    <option value={p}>{p}</option>
                {/each}
            </select>
        </div>

        <div class="question">
            <label for="sel-estrato">Estrato socioeconómico</label>
            <select id="sel-estrato" bind:value={perfil.estrato}>
                <option value="" disabled>Seleccionar…</option>
                {#each OPCIONES.estrato as e}
                    <option value={e}>{e}</option>
                {/each}
            </select>
        </div>

        <div class="question">
            <label for="sel-colegio">Tipo de colegio de procedencia</label>
            <select id="sel-colegio" bind:value={perfil.tipo_colegio}>
                <option value="" disabled>Seleccionar…</option>
                {#each OPCIONES.tipo_colegio as c}
                    <option value={c}>{c}</option>
                {/each}
            </select>
        </div>

        <div class="question">
            <label for="sel-genero">Género</label>
            <select id="sel-genero" bind:value={perfil.genero}>
                <option value="" disabled>Seleccionar…</option>
                {#each OPCIONES.genero as g}
                    <option value={g}>{g}</option>
                {/each}
            </select>
        </div>

        <div class="question">
            <label for="sel-mat">¿Requirió nivelación en matemáticas?</label>
            <select id="sel-mat" bind:value={perfil.nivelacion_matematicas}>
                <option value="NO">No</option>
                <option value="SI">Sí</option>
            </select>
        </div>

        <div class="question">
            <label for="sel-lecto">¿Requirió nivelación en lectoescritura?</label>
            <select id="sel-lecto" bind:value={perfil.nivelacion_lectoescritura}>
                <option value="NO">No</option>
                <option value="SI">Sí</option>
            </select>
        </div>
    </form>

    <h2>Riesgo Temprano</h2>

    {#if riesgo !== null}
        <div transition:fade={{ duration: 200 }}>
            <Riesgo {riesgo} />
        </div>
    {:else}
        <p class="pendiente">Completa los primeros cuatro campos para ver el resultado.</p>
    {/if}

    <details class="metodologia">
        <summary>¿Cómo funciona el modelo?</summary>
        <p>
            Se usa un <strong>modelo multiplicativo de riesgo</strong> (equivalente a una
            regresión logística con coeficientes calculados directamente desde datos
            observados). Para cada variable se calcula el <em>log risk ratio</em>:
        </p>
        <pre>coef[variable][categoría] = log( tasa_categoría / tasa_base )</pre>
        <p>
            La predicción combina todos los coeficientes via log-odds y aplica una
            función sigmoide para obtener una probabilidad en [0, 1].
        </p>
        <p>
            <strong>Fuente:</strong> dashboard público de UNAL Sede Bogotá en Tableau Public,
            periodo 2025-2. Tasa base global: 5.07 %.
        </p>
        <p>
            <strong>Limitación:</strong> los datos son agregados por categoría, no registros
            individuales. El modelo asume independencia entre variables (supuesto de Naive
            Bayes), lo que es una simplificación. Úsalo como ejercicio educativo, no como
            diagnóstico clínico.
        </p>
    </details>
</div>

{#if esAlto}
    <div transition:fade={{ duration: 300 }}>
        <AlertaTemprana />
    </div>
{/if}

<style>
    #container {
        max-width: 520px;
        width: 100%;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: stretch;
        gap: 0.25rem;
    }

    .intro {
        opacity: 0.75;
        font-size: 0.9rem;
        margin: 0 0 0.5rem;
    }

    .tarjeta {
        background: #B069DB;
        color: #fff;
        border-radius: 0.75rem;
        padding: 1.25rem 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
    }

    .question {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    label {
        flex: 1;
        font-size: 0.92rem;
    }

    select {
        appearance: base-select;
        min-width: 11rem;
        max-width: 11rem;
        font-size: 0.92rem;
        color: #fff;
    }

    select option {
        background: Canvas;
        color: CanvasText;
    }

    .pendiente {
        opacity: 0.55;
        font-size: 0.9rem;
        text-align: center;
    }

    .metodologia {
        margin-top: 1.5rem;
        font-size: 0.85rem;
        opacity: 0.75;
        border-top: 1px solid color-mix(in srgb, currentColor 15%, transparent);
        padding-top: 0.75rem;
    }

    .metodologia summary {
        cursor: pointer;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .metodologia pre {
        background: color-mix(in srgb, currentColor 8%, transparent);
        padding: 0.5rem 0.75rem;
        border-radius: 0.4rem;
        font-size: 0.8rem;
        overflow-x: auto;
    }

    .metodologia p {
        margin: 0.4rem 0;
    }
</style>
