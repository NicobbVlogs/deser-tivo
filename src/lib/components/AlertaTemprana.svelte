<script lang="ts">
    import { fade, slide } from "svelte/transition";

    // ── Sección A ────────────────────────────────────────────────────────────
    let papa = $state(3.5);
    let creditosAprobados = $state(12);
    let creditosMatriculados = $state(15);
    let asistencia = $state(80);
    let materiasReprobadas = $state("0");
    let semestre = $state("3°");
    let moodle = $state("Alta (>5 accesos)");

    // ── Sección B ────────────────────────────────────────────────────────────
    let estrato = $state("3");
    let trabaja = $state(false);
    let horasTrabajo = $state(20);
    let beca = $state(false);
    let dependientes = $state(false);
    let distancia = $state("< 30 min");

    // ── Sección C ────────────────────────────────────────────────────────────
    let psicologia = $state(false);
    let estres = $state(5);
    let faltasExamen = $state("Nunca");

    // ── Sección D (Likert 1–5, índices 0–4) ─────────────────────────────────
    let likert = $state([3, 3, 3, 3, 3]);

    const LIKERT_PREGUNTAS = [
        "Me siento motivado/a con mi carrera",
        "Siento que puedo superar los retos académicos del semestre",
        "Tengo apoyo de familia o amigos cercanos",
        "He pensado en cambiarme de carrera/universidad este semestre",
        "Siento que tengo suficientes recursos económicos",
    ];

    // ── Estado de resultados ─────────────────────────────────────────────────
    let mostrarResultados = $state(false);

    // ── Puntaje (0–100) ──────────────────────────────────────────────────────
    const puntaje = $derived.by(() => {
        if (!mostrarResultados) return 0;
        let p = 0;

        if (papa < 2.5) p += 25;
        else if (papa <= 3.2) p += 12;

        if (asistencia < 50) p += 20;
        else if (asistencia <= 70) p += 10;

        const rep = materiasReprobadas === "5+" ? 5 : +materiasReprobadas;
        if (rep > 2) p += 15;
        else if (rep >= 1) p += 8;

        if (moodle === "Nula (sin acceso)") p += 15;
        else if (moodle.startsWith("Baja")) p += 8;
        else if (moodle.startsWith("Media")) p += 3;

        if (trabaja) {
            if (horasTrabajo > 30) p += 12;
            else if (horasTrabajo >= 15) p += 6;
        }

        if (!beca && +estrato <= 2) p += 8;

        if (estres > 7) p += 10;
        else if (estres >= 5) p += 4;

        if (faltasExamen === "Más de 3 veces") p += 12;
        else if (faltasExamen === "2-3 veces") p += 6;
        else if (faltasExamen === "1 vez") p += 2;

        if (likert[3] >= 4) p += 10;
        else if (likert[3] === 3) p += 4;

        if (likert[0] <= 2) p += 8;
        else if (likert[0] === 3) p += 3;

        if (likert[4] <= 2) p += 6;

        if (dependientes) p += 5;
        if (distancia === "> 2 horas") p += 5;

        return Math.min(100, p);
    });

    const nivel = $derived(puntaje >= 66 ? "alto" : puntaje >= 36 ? "medio" : "bajo");

    // ── Factores individuales (0–100) ────────────────────────────────────────
    const factores = $derived.by(() => {
        if (!mostrarResultados) return null;

        const rep = materiasReprobadas === "5+" ? 5 : +materiasReprobadas;
        const e = +estrato;

        let rendimiento = 0;
        if (papa < 2.5) rendimiento += 50;
        else if (papa <= 3.2) rendimiento += 30;
        const ratio = creditosMatriculados > 0 ? creditosAprobados / creditosMatriculados : 1;
        if (ratio < 0.5) rendimiento += 30;
        else if (ratio < 0.75) rendimiento += 15;
        if (rep > 2) rendimiento += 20;
        else if (rep >= 1) rendimiento += 10;

        let compromiso = 0;
        if (asistencia < 50) compromiso += 50;
        else if (asistencia <= 70) compromiso += 30;
        if (moodle === "Nula (sin acceso)") compromiso += 50;
        else if (moodle.startsWith("Baja")) compromiso += 25;
        else if (moodle.startsWith("Media")) compromiso += 10;

        let socioeco = 0;
        if (e <= 1) socioeco += 30;
        else if (e <= 2) socioeco += 20;
        else if (e <= 3) socioeco += 10;
        if (trabaja && horasTrabajo > 30) socioeco += 30;
        else if (trabaja && horasTrabajo >= 15) socioeco += 15;
        if (!beca && e <= 2) socioeco += 20;
        if (dependientes) socioeco += 15;
        if (distancia === "> 2 horas") socioeco += 10;

        let bienestar = 0;
        if (estres > 7) bienestar += 40;
        else if (estres >= 5) bienestar += 20;
        if (faltasExamen === "Más de 3 veces") bienestar += 40;
        else if (faltasExamen === "2-3 veces") bienestar += 25;
        else if (faltasExamen === "1 vez") bienestar += 10;
        if (!psicologia && estres > 6) bienestar += 20;

        let apoyo = 0;
        if (likert[2] <= 2) apoyo += 40;
        else if (likert[2] === 3) apoyo += 20;
        if (likert[0] <= 2) apoyo += 35;
        else if (likert[0] === 3) apoyo += 15;
        if (likert[3] >= 4) apoyo += 25;

        return {
            rendimiento: Math.min(100, rendimiento),
            compromiso:  Math.min(100, compromiso),
            socioeco:    Math.min(100, socioeco),
            bienestar:   Math.min(100, bienestar),
            apoyo:       Math.min(100, apoyo),
        };
    });

    // ── Señales de alerta ────────────────────────────────────────────────────
    const señales = $derived.by((): string[] => {
        if (!mostrarResultados) return [];
        const s: string[] = [];

        if (papa < 2.5)
            s.push(`P.A.P.A. de ${papa.toFixed(1)} por debajo del umbral crítico (2.5)`);
        else if (papa <= 3.2)
            s.push(`P.A.P.A. de ${papa.toFixed(1)} en zona de alerta (2.5–3.2)`);

        if (asistencia < 50)
            s.push(`Asistencia del ${asistencia}% (umbral crítico < 50%)`);
        else if (asistencia <= 70)
            s.push(`Asistencia del ${asistencia}% (por debajo del 70% recomendado)`);

        if (moodle === "Nula (sin acceso)")
            s.push("Sin acceso a plataforma virtual en las últimas 2 semanas");

        if (trabaja && horasTrabajo > 30)
            s.push(`Estrato ${estrato} trabajando ${horasTrabajo}h/semana (carga alta)`);
        else if (trabaja && horasTrabajo >= 15)
            s.push(`Trabaja ${horasTrabajo}h/semana en paralelo con estudios`);

        if (!beca && +estrato <= 2)
            s.push(`Estrato ${estrato} sin beca ni apoyo de bienestar`);

        if (estres > 7)
            s.push(`Nivel de estrés ${estres}/10 (nivel crítico)`);

        if (faltasExamen !== "Nunca")
            s.push(`${faltasExamen} de ausencias injustificadas en evaluaciones`);

        if (likert[3] >= 4)
            s.push("Pensamiento activo de cambio de carrera o universidad");

        return s.slice(0, 5);
    });

    // ── Intervención recomendada ─────────────────────────────────────────────
    const intervencion = $derived.by(() => {
        if (!mostrarResultados || !factores) return null;
        const f = factores;
        const maxVal = Math.max(f.rendimiento, f.compromiso, f.socioeco, f.bienestar, f.apoyo);

        let tipo = "", icono = "", texto = "";

        if (maxVal === f.rendimiento || (maxVal === f.compromiso && f.rendimiento >= f.socioeco)) {
            tipo = "Tutoría Académica"; icono = "📚";
            texto = `Dado su P.A.P.A. de ${papa.toFixed(1)} y una asistencia del ${asistencia}%, se recomienda vinculación inmediata al programa de tutorías pares.`;
            if (moodle === "Nula (sin acceso)")
                texto += " La ausencia total en plataformas virtuales indica desconexión activa del proceso académico.";
        } else if (maxVal === f.bienestar) {
            tipo = "Atención Psicológica"; icono = "💚";
            texto = `Con un nivel de estrés de ${estres}/10${faltasExamen !== "Nunca" ? ` y ${faltasExamen.toLowerCase()} de ausencias injustificadas` : ""}, se recomienda orientación con Bienestar Universitario para acompañamiento emocional y manejo del estrés.`;
        } else if (maxVal === f.socioeco) {
            tipo = "Trabajo Social"; icono = "💼";
            texto = `El perfil socioeconómico (estrato ${estrato}${trabaja ? `, trabajando ${horasTrabajo}h/semana` : ""}${!beca ? ", sin apoyo de bienestar" : ""}) indica necesidad de gestión de apoyos económicos y servicios estudiantiles.`;
        } else {
            tipo = "Orientación y Acompañamiento"; icono = "🤝";
            texto = likert[3] >= 4
                ? "La intención de cambio de carrera sugiere necesidad de orientación vocacional y exploración de opciones dentro de la universidad."
                : "Se detecta debilitamiento en la red de apoyo personal. Se recomienda vinculación con grupos estudiantiles y espacios de mentoría.";
        }

        const prioridad =
            nivel === "alto"  ? "Intervención inmediata" :
            nivel === "medio" ? "Seguimiento en 2 semanas" :
                                "Monitoreo preventivo";

        return { tipo, icono, texto, prioridad };
    });

    // ── Helpers de color ─────────────────────────────────────────────────────
    function colorFactor(v: number): string {
        return v >= 66 ? "#e53935" : v >= 36 ? "#f59e0b" : "#43a047";
    }

    function nivelColor(n: string): string {
        return n === "alto" ? "#e53935" : n === "medio" ? "#f59e0b" : "#43a047";
    }

    function nivelLabel(n: string): string {
        return n === "alto" ? "🔴 RIESGO ALTO" : n === "medio" ? "🟡 RIESGO MEDIO" : "🟢 RIESGO BAJO";
    }
</script>

<section class="alerta-temprana">
    <div class="alerta-header">
        <h2>Análisis de Alerta Temprana</h2>
        <p class="subtexto">
            Formulario ampliado — factores académicos, socioeconómicos y de bienestar.
            Completa el perfil y presiona <strong>Analizar</strong> para ver el desglose.
        </p>
    </div>

    <div class="dos-columnas">

        <!-- ══ COLUMNA IZQUIERDA ══════════════════════════════════════════════ -->
        <div class="col-izq">

            <!-- Sección A -->
            <details class="seccion" open>
                <summary>A · Datos Académicos</summary>
                <div class="campo-grupo">

                    <div class="campo">
                        <label>Promedio actual (P.A.P.A.): <strong>{papa.toFixed(1)}</strong></label>
                        <input type="range" min="0" max="5" step="0.1" bind:value={papa} />
                    </div>

                    <div class="campo fila">
                        <div class="sub-campo">
                            <label>Créditos aprobados</label>
                            <input type="number" min="0" max="20" bind:value={creditosAprobados} />
                        </div>
                        <div class="sub-campo">
                            <label>Créditos matriculados</label>
                            <input type="number" min="1" max="20" bind:value={creditosMatriculados} />
                        </div>
                    </div>

                    <div class="campo">
                        <label>Asistencia a clases: <strong>{asistencia}%</strong></label>
                        <input type="range" min="0" max="100" step="5" bind:value={asistencia} />
                    </div>

                    <div class="campo">
                        <label>Materias reprobadas (historial)</label>
                        <select bind:value={materiasReprobadas}>
                            {#each ["0","1","2","3","4","5+"] as v}
                                <option value={v}>{v}</option>
                            {/each}
                        </select>
                    </div>

                    <div class="campo">
                        <label>Semestre actual</label>
                        <select bind:value={semestre}>
                            {#each ["1°","2°","3°","4°","5°","6°","7°","8°","9°","10°"] as s}
                                <option value={s}>{s}</option>
                            {/each}
                        </select>
                    </div>

                    <div class="campo">
                        <label>Participación en plataforma virtual (últimas 2 semanas)</label>
                        <select bind:value={moodle}>
                            <option>Alta ({">"}>5 accesos)</option>
                            <option>Media (2-5 accesos)</option>
                            <option>Baja (1-2 accesos)</option>
                            <option>Nula (sin acceso)</option>
                        </select>
                    </div>

                </div>
            </details>

            <!-- Sección B -->
            <details class="seccion" open>
                <summary>B · Factores Socioeconómicos</summary>
                <div class="campo-grupo">

                    <div class="campo">
                        <label>Estrato socioeconómico</label>
                        <select bind:value={estrato}>
                            {#each ["1","2","3","4","5","6"] as e}
                                <option value={e}>{e}</option>
                            {/each}
                        </select>
                    </div>

                    <div class="campo fila-toggle">
                        <label>¿Trabaja actualmente?</label>
                        <button
                            type="button"
                            class="toggle {trabaja ? 'activo' : ''}"
                            onclick={() => trabaja = !trabaja}
                        >{trabaja ? "Sí" : "No"}</button>
                    </div>

                    {#if trabaja}
                        <div class="campo" transition:slide={{ duration: 200 }}>
                            <label>Horas de trabajo por semana: <strong>{horasTrabajo}h</strong></label>
                            <input type="range" min="0" max="60" step="1" bind:value={horasTrabajo} />
                        </div>
                    {/if}

                    <div class="campo fila-toggle">
                        <label>¿Recibe beca o apoyo de bienestar?</label>
                        <button
                            type="button"
                            class="toggle {beca ? 'activo' : ''}"
                            onclick={() => beca = !beca}
                        >{beca ? "Sí" : "No"}</button>
                    </div>

                    <div class="campo fila-toggle">
                        <label>¿Tiene dependientes económicos?</label>
                        <button
                            type="button"
                            class="toggle {dependientes ? 'activo' : ''}"
                            onclick={() => dependientes = !dependientes}
                        >{dependientes ? "Sí" : "No"}</button>
                    </div>

                    <div class="campo">
                        <label>Distancia al campus</label>
                        <select bind:value={distancia}>
                            <option>{"< 30 min"}</option>
                            <option>30-60 min</option>
                            <option>1-2 horas</option>
                            <option>{"> 2 horas"}</option>
                        </select>
                    </div>

                </div>
            </details>

            <!-- Sección C -->
            <details class="seccion" open>
                <summary>C · Bienestar y Salud</summary>
                <div class="campo-grupo">

                    <div class="campo fila-toggle">
                        <label>¿Ha visitado psicología o bienestar este semestre?</label>
                        <button
                            type="button"
                            class="toggle {psicologia ? 'activo' : ''}"
                            onclick={() => psicologia = !psicologia}
                        >{psicologia ? "Sí" : "No"}</button>
                    </div>

                    <div class="campo">
                        <label>Nivel de estrés percibido: <strong>{estres}/10</strong></label>
                        <input type="range" min="1" max="10" step="1" bind:value={estres} />
                        <span class="escala-hint">1 = muy bajo · 10 = muy alto</span>
                    </div>

                    <div class="campo">
                        <label>¿Ha faltado a exámenes/entregas sin justificación?</label>
                        <select bind:value={faltasExamen}>
                            <option>Nunca</option>
                            <option>1 vez</option>
                            <option>2-3 veces</option>
                            <option>Más de 3 veces</option>
                        </select>
                    </div>

                </div>
            </details>

            <!-- Sección D -->
            <details class="seccion" open>
                <summary>D · Cuestionario Breve (Autoreporte)</summary>
                <div class="campo-grupo">
                    <p class="likert-escala">1 = Totalmente en desacuerdo · 5 = Totalmente de acuerdo</p>

                    {#each LIKERT_PREGUNTAS as pregunta, i}
                        <div class="likert-pregunta">
                            <p class="likert-texto">{pregunta}</p>
                            <div class="likert-opciones">
                                {#each [1, 2, 3, 4, 5] as val}
                                    <label class="likert-radio">
                                        <input
                                            type="radio"
                                            name="likert-{i}"
                                            value={val}
                                            checked={likert[i] === val}
                                            onchange={() => { likert[i] = val; }}
                                        />
                                        <span class="likert-num">{val}</span>
                                    </label>
                                {/each}
                            </div>
                        </div>
                    {/each}
                </div>
            </details>

            <button
                type="button"
                class="btn-analizar"
                onclick={() => mostrarResultados = true}
            >
                🔍 Analizar Perfil de Riesgo
            </button>
        </div>

        <!-- ══ COLUMNA DERECHA ════════════════════════════════════════════════ -->
        <div class="col-der">
            {#if !mostrarResultados}
                <div class="estado-vacio">
                    <span class="vacio-icono">🎓</span>
                    <p>Complete el perfil del estudiante y presione <strong>Analizar</strong> para ver el resultado.</p>
                </div>
            {:else}
                <div class="tarjeta-resultado" transition:fade={{ duration: 250 }}>

                    <!-- Badge de nivel -->
                    <div class="nivel-badge" style="--col: {nivelColor(nivel)}">
                        <span class="nivel-texto">{nivelLabel(nivel)}</span>
                        <span class="nivel-puntaje">Puntuación: {puntaje} / 100</span>
                    </div>

                    <!-- Barra de puntaje -->
                    <div class="barra-fondo">
                        <div
                            class="barra-relleno"
                            style="width: {puntaje}%; background: {nivelColor(nivel)}"
                        ></div>
                    </div>

                    {#if factores}
                    <!-- Desglose de factores -->
                    <div class="bloque">
                        <h4>Factores de Riesgo Detectados</h4>
                        {#each [
                            { nombre: "Rendimiento académico",     valor: factores.rendimiento },
                            { nombre: "Compromiso con el estudio", valor: factores.compromiso  },
                            { nombre: "Situación socioeconómica",  valor: factores.socioeco    },
                            { nombre: "Bienestar emocional",       valor: factores.bienestar   },
                            { nombre: "Red de apoyo personal",     valor: factores.apoyo       },
                        ] as f}
                            <div class="factor">
                                <div class="factor-cabecera">
                                    <span>{f.nombre}</span>
                                    <span style="color: {colorFactor(f.valor)}; font-weight: 600">{f.valor}</span>
                                </div>
                                <div class="factor-barra-fondo">
                                    <div
                                        class="factor-barra-relleno"
                                        style="width: {f.valor}%; background: {colorFactor(f.valor)}"
                                    ></div>
                                </div>
                            </div>
                        {/each}
                    </div>
                    {/if}

                    {#if intervencion}
                    <!-- Intervención recomendada -->
                    <div class="bloque">
                        <h4>Intervención Recomendada</h4>
                        <div class="intervencion">
                            <div class="intervencion-tipo">
                                <span class="intervencion-icono">{intervencion.icono}</span>
                                <span class="intervencion-nombre">{intervencion.tipo}</span>
                            </div>
                            <p class="intervencion-texto">{intervencion.texto}</p>
                            <span class="prioridad">⚡ {intervencion.prioridad}</span>
                        </div>
                    </div>
                    {/if}

                    {#if señales.length > 0}
                    <!-- Señales clave -->
                    <div class="bloque">
                        <h4>Señales Clave</h4>
                        <ul class="señales">
                            {#each señales as s}
                                <li>⚠ {s}</li>
                            {/each}
                        </ul>
                    </div>
                    {/if}

                    <p class="disclaimer">
                        Este análisis es generado por un modelo de demostración. En producción,
                        el sistema utilizará datos reales del SIA y Moodle de la UNAL.
                    </p>
                </div>
            {/if}
        </div>

    </div>
</section>

<style>
    /* ── Wrapper ──────────────────────────────────────────────────────────── */
    .alerta-temprana {
        margin-top: 2.5rem;
        padding-top: 2rem;
        border-top: 2px solid rgba(176, 105, 219, 0.3);
    }

    .alerta-header {
        margin-bottom: 1.25rem;
    }

    .alerta-header h2 {
        font-family: "Sekuya", serif;
        letter-spacing: 2px;
        margin: 0 0 0.35rem;
    }

    .subtexto {
        font-size: 0.85rem;
        opacity: 0.65;
        margin: 0;
    }

    /* ── Grid dos columnas ────────────────────────────────────────────────── */
    .dos-columnas {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.25rem;
        align-items: start;
    }

    @media (max-width: 680px) {
        .dos-columnas { grid-template-columns: 1fr; }
    }

    /* ── Secciones acordeón ───────────────────────────────────────────────── */
    .seccion {
        background: #B069DB;
        color: #fff;
        border-radius: 0.75rem;
        margin-bottom: 0.65rem;
        overflow: hidden;
    }

    .seccion > summary {
        padding: 0.7rem 1.1rem;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.9rem;
        list-style: none;
        user-select: none;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .seccion > summary::before {
        content: "▸";
        display: inline-block;
        transition: transform 0.18s;
        font-size: 0.75rem;
        opacity: 0.7;
    }

    .seccion[open] > summary::before {
        transform: rotate(90deg);
    }

    /* ── Campos ───────────────────────────────────────────────────────────── */
    .campo-grupo {
        padding: 0.4rem 1.1rem 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.7rem;
        border-top: 1px solid rgba(255 255 255 / 0.15);
    }

    .campo {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .campo label {
        font-size: 0.85rem;
        opacity: 0.9;
    }

    .campo.fila {
        flex-direction: row;
        gap: 0.75rem;
    }

    .sub-campo {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .campo.fila-toggle {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
    }

    .campo input[type="range"] {
        width: 100%;
        accent-color: rgba(255 255 255 / 0.9);
        cursor: pointer;
    }

    .campo input[type="number"] {
        background: rgba(255 255 255 / 0.15);
        color: #fff;
        border: 1px solid rgba(255 255 255 / 0.3);
        border-radius: 0.4rem;
        padding: 0.3rem 0.45rem;
        font-size: 0.85rem;
        width: 100%;
        font-family: inherit;
    }

    .campo select {
        background: rgba(255 255 255 / 0.15);
        color: #fff;
        border: 1px solid rgba(255 255 255 / 0.3);
        border-radius: 0.4rem;
        padding: 0.3rem 0.45rem;
        font-size: 0.85rem;
        font-family: inherit;
        appearance: base-select;
    }

    .campo select option {
        background: Canvas;
        color: CanvasText;
    }

    .escala-hint {
        font-size: 0.72rem;
        opacity: 0.6;
    }

    /* ── Toggle ───────────────────────────────────────────────────────────── */
    .toggle {
        background: rgba(255 255 255 / 0.15);
        color: #fff;
        border: 1px solid rgba(255 255 255 / 0.35);
        border-radius: 1rem;
        padding: 0.2rem 0.75rem;
        font-size: 0.82rem;
        cursor: pointer;
        transition: background 0.15s;
        min-width: 3.2rem;
        text-align: center;
        font-family: inherit;
        flex-shrink: 0;
    }

    .toggle.activo {
        background: rgba(255 255 255 / 0.88);
        color: #7B3ABF;
        border-color: #fff;
        font-weight: 600;
    }

    /* ── Likert ───────────────────────────────────────────────────────────── */
    .likert-escala {
        font-size: 0.75rem;
        opacity: 0.65;
        margin: 0;
    }

    .likert-pregunta {
        margin-bottom: 0.4rem;
    }

    .likert-texto {
        font-size: 0.83rem;
        margin: 0 0 0.3rem;
        opacity: 0.95;
    }

    .likert-opciones {
        display: flex;
        gap: 0.6rem;
    }

    .likert-radio {
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
        gap: 0.1rem;
    }

    .likert-radio input[type="radio"] {
        accent-color: #fff;
        cursor: pointer;
    }

    .likert-num {
        font-size: 0.72rem;
        opacity: 0.75;
    }

    /* ── Botón analizar ───────────────────────────────────────────────────── */
    .btn-analizar {
        width: 100%;
        padding: 0.8rem;
        background: #7B3ABF;
        color: #fff;
        border: none;
        border-radius: 0.75rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        margin-top: 0.25rem;
        transition: background 0.15s;
        font-family: inherit;
    }

    .btn-analizar:hover {
        background: #6A2FA8;
    }

    /* ── Columna derecha ──────────────────────────────────────────────────── */
    .estado-vacio {
        background: rgba(176, 105, 219, 0.08);
        border: 2px dashed rgba(176, 105, 219, 0.3);
        border-radius: 0.75rem;
        padding: 3rem 1.5rem;
        text-align: center;
        opacity: 0.7;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.75rem;
    }

    .vacio-icono { font-size: 2.5rem; }

    .tarjeta-resultado {
        background: #B069DB;
        color: #fff;
        border-radius: 0.75rem;
        padding: 1.25rem 1.4rem;
        display: flex;
        flex-direction: column;
        gap: 1.1rem;
    }

    /* Badge de nivel */
    .nivel-badge {
        text-align: center;
        background: rgba(255 255 255 / 0.12);
        border: 2px solid var(--col);
        border-radius: 0.6rem;
        padding: 0.85rem 1rem;
    }

    .nivel-texto {
        display: block;
        font-size: 1.3rem;
        font-weight: 700;
        font-family: "Sekuya", serif;
        letter-spacing: 1px;
        color: var(--col);
        text-shadow: 0 1px 3px rgba(0 0 0 / 0.25);
    }

    .nivel-puntaje {
        display: block;
        font-size: 0.85rem;
        opacity: 0.8;
        margin-top: 0.3rem;
    }

    /* Barra de puntaje */
    .barra-fondo {
        background: rgba(255 255 255 / 0.2);
        border-radius: 1rem;
        height: 0.55rem;
        overflow: hidden;
    }

    .barra-relleno {
        height: 100%;
        border-radius: 1rem;
        transition: width 0.4s ease;
        min-width: 0.3rem;
    }

    /* Bloques interiores */
    .bloque { display: flex; flex-direction: column; gap: 0.5rem; }

    .bloque h4 {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.65;
        margin: 0;
    }

    /* Barras de factores */
    .factor { display: flex; flex-direction: column; gap: 0.2rem; }

    .factor-cabecera {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        opacity: 0.9;
    }

    .factor-barra-fondo {
        background: rgba(255 255 255 / 0.2);
        border-radius: 1rem;
        height: 0.4rem;
        overflow: hidden;
    }

    .factor-barra-relleno {
        height: 100%;
        border-radius: 1rem;
        transition: width 0.35s ease;
        min-width: 0.2rem;
    }

    /* Intervención */
    .intervencion {
        background: rgba(255 255 255 / 0.12);
        border-radius: 0.55rem;
        padding: 0.75rem 0.9rem;
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }

    .intervencion-tipo {
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }

    .intervencion-icono { font-size: 1.2rem; }

    .intervencion-nombre {
        font-weight: 600;
        font-size: 0.9rem;
    }

    .intervencion-texto {
        font-size: 0.82rem;
        line-height: 1.5;
        opacity: 0.9;
        margin: 0;
    }

    .prioridad {
        display: inline-block;
        background: rgba(255 255 255 / 0.18);
        border-radius: 1rem;
        padding: 0.18rem 0.65rem;
        font-size: 0.76rem;
        font-weight: 600;
        align-self: flex-start;
    }

    /* Señales */
    .señales {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .señales li {
        font-size: 0.8rem;
        opacity: 0.88;
        padding: 0.25rem 0;
        border-bottom: 1px solid rgba(255 255 255 / 0.1);
    }

    .señales li:last-child { border-bottom: none; }

    /* Disclaimer */
    .disclaimer {
        font-size: 0.7rem;
        opacity: 0.45;
        text-align: center;
        margin: 0;
        line-height: 1.5;
    }
</style>
