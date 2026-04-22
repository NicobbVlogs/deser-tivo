<script lang="ts">
    import { TASA_BASE, RIESGO_MAX } from "$lib/modelo";
    import wake from "$lib/assets/RESULTADOS/WAKE UP.gif";
    import perrito from "$lib/assets/RESULTADOS/SAQUENME DE AQUI.jpeg";
    import popozao from "$lib/assets/RESULTADOS/TREME POPAZAO.gif";

    const { riesgo }: { riesgo: number } = $props();

    const porcentaje = $derived(Math.round(riesgo * 100));
    const base = Math.round(TASA_BASE * 100);
    const maxPct = Math.round(RIESGO_MAX * 100);
    const diferencia = $derived(Math.round((riesgo - TASA_BASE) * 100));

    // Posiciones en la barra relativa (0 → máx alcanzable)
    const barraRelleno = $derived(Math.min(100, (riesgo / RIESGO_MAX) * 100));
    const barraMarca = Math.min(100, (TASA_BASE / RIESGO_MAX) * 100);
</script>

<div class="resultado">
    <!-- Cifra absoluta -->
    <p class="cifra">{porcentaje} <span class="de-cien">/ 100</span></p>
    <p class="subtexto">probabilidad estimada de deserción</p>

    <!-- Barra relativa al máximo alcanzable -->
    <div class="barra-fondo">
        <div class="barra-relleno" style="width: {barraRelleno}%"></div>
        <!-- Marca del promedio UNAL sobre la escala relativa -->
        <div
            class="barra-marca"
            style="left: {barraMarca}%"
            title="promedio UNAL ({base} %)"
        ></div>
    </div>
    <div class="barra-etiquetas">
        <span>0 %</span>
        <span class="marca-label" style="left: {barraMarca}%"
            >prom. {base} %</span
        >
        <span>máx. {maxPct} %</span>
    </div>

    <!-- Diferencia en puntos porcentuales -->
    <p class="comparativa">
        {#if diferencia > 0}
            <span class="sube">+{diferencia} pp</span> respecto al promedio UNAL
            ({base} %)
        {:else if diferencia < 0}
            <span class="baja">{diferencia} pp</span> respecto al promedio UNAL
            ({base} %)
        {:else}
            Igual al promedio UNAL ({base} %)
        {/if}
    </p>

    {#if riesgo > 0.12}
        <p class="nivel high">Riesgo alto</p>
        <img alt="Perrito triste" src={perrito} />
    {:else if riesgo > 0.07}
        <p class="nivel moderate">Riesgo moderado</p>
        <img
            alt="Señor en el piso con un reloj sobre él, intentándolo despertar"
            src={wake}
        />
    {:else}
        <p class="nivel low">Riesgo bajo</p>
        <img
            alt="Señor en el piso con un reloj sobre él, intentándolo despertar"
            src={popozao}
        />
    {/if}
</div>

<style>
    .resultado {
        text-align: center;
        padding: 1.5rem;
        border-radius: 0.75rem;
        background: #b069db;
        color: #fff;
        width: 100%;
    }

    .cifra {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        line-height: 1;
    }

    .de-cien {
        font-size: 1.4rem;
        font-weight: 400;
        opacity: 0.75;
    }

    .subtexto {
        font-size: 0.85rem;
        opacity: 0.8;
        margin: 0.3rem 0 1rem;
    }

    /* Barra relativa al máximo alcanzable */
    .barra-fondo {
        position: relative;
        background: rgba(255 255 255 / 0.25);
        border-radius: 1rem;
        height: 0.75rem;
        margin: 0 0.25rem;
    }

    .barra-relleno {
        height: 100%;
        border-radius: 1rem;
        background: #fff;
        transition: width 0.35s ease;
        min-width: 0.4rem;
    }

    /* Línea vertical: promedio UNAL */
    .barra-marca {
        position: absolute;
        top: -0.25rem;
        bottom: -0.25rem;
        width: 2px;
        background: rgba(255 255 255 / 0.6);
        border-radius: 1px;
        transform: translateX(-50%);
    }

    .barra-etiquetas {
        position: relative;
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
        opacity: 0.7;
        margin: 0.25rem 0.25rem 0;
        height: 1rem;
    }

    /* Etiqueta flotante para el promedio */
    .marca-label {
        position: absolute;
        transform: translateX(-50%);
        white-space: nowrap;
    }

    .comparativa {
        font-size: 0.9rem;
        margin: 0.75rem 0;
        opacity: 0.9;
    }

    .sube {
        font-weight: 700;
    }
    .baja {
        font-weight: 700;
    }

    img {
        display: block;
        margin: auto;
        margin-top: 1rem;
        border-radius: 1rem;
        max-width: 80%;
    }

    .nivel {
        display: inline-block;
        padding: 0.25rem 1rem;
        border-radius: 1rem;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0;
        background: rgba(255 255 255 / 0.2);
        color: #fff;
    }
</style>
