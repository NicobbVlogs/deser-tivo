<script lang="ts">
    import { fade, slide } from "svelte/transition";
    import dinero from "$lib/assets/RESULTADOS/DINERO.jpeg";
    import loro from "$lib/assets/RESULTADOS/LORO.jpeg";

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

    // ── Estado ───────────────────────────────────────────────────────────────
    let mostrarResultados = $state(false);

    // ── Randomizar ───────────────────────────────────────────────────────────
    function randomizar() {
        const pick = <T,>(arr: T[]) => arr[Math.floor(Math.random() * arr.length)];
        papa = Math.round(Math.random() * 50) / 10;
        creditosAprobados = Math.floor(Math.random() * 17);
        creditosMatriculados = Math.min(20, creditosAprobados + Math.floor(Math.random() * 5) + 1);
        asistencia = Math.round(Math.random() * 20) * 5;
        materiasReprobadas = pick(["0","1","2","3","4","5+"]);
        semestre = pick(["1°","2°","3°","4°","5°","6°","7°","8°","9°","10°"]);
        moodle = pick(["Alta (>5 accesos)","Media (2-5 accesos)","Baja (1-2 accesos)","Nula (sin acceso)"]);
        estrato = String(Math.floor(Math.random() * 6) + 1);
        trabaja = Math.random() > 0.5;
        horasTrabajo = Math.floor(Math.random() * 61);
        beca = Math.random() > 0.5;
        dependientes = Math.random() > 0.7;
        distancia = pick(["< 30 min","30-60 min","1-2 horas","> 2 horas"]);
        psicologia = Math.random() > 0.7;
        estres = Math.floor(Math.random() * 10) + 1;
        faltasExamen = pick(["Nunca","1 vez","2-3 veces","Más de 3 veces"]);
        for (let i = 0; i < 5; i++) likert[i] = Math.floor(Math.random() * 5) + 1;
        mostrarResultados = true;
    }

    // ── Puntaje (0–100) ──────────────────────────────────────────────────────
    const puntaje = $derived.by(() => {
        if (!mostrarResultados) return 0;
        let p = 0;
        if (papa < 2.5) p += 25; else if (papa <= 3.2) p += 12;
        if (asistencia < 50) p += 20; else if (asistencia <= 70) p += 10;
        const rep = materiasReprobadas === "5+" ? 5 : +materiasReprobadas;
        if (rep > 2) p += 15; else if (rep >= 1) p += 8;
        if (moodle === "Nula (sin acceso)") p += 15;
        else if (moodle.startsWith("Baja")) p += 8;
        else if (moodle.startsWith("Media")) p += 3;
        if (trabaja) { if (horasTrabajo > 30) p += 12; else if (horasTrabajo >= 15) p += 6; }
        if (!beca && +estrato <= 2) p += 8;
        if (estres > 7) p += 10; else if (estres >= 5) p += 4;
        if (faltasExamen === "Más de 3 veces") p += 12;
        else if (faltasExamen === "2-3 veces") p += 6;
        else if (faltasExamen === "1 vez") p += 2;
        if (likert[3] >= 4) p += 10; else if (likert[3] === 3) p += 4;
        if (likert[0] <= 2) p += 8; else if (likert[0] === 3) p += 3;
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
        if (papa < 2.5) rendimiento += 50; else if (papa <= 3.2) rendimiento += 30;
        const ratio = creditosMatriculados > 0 ? creditosAprobados / creditosMatriculados : 1;
        if (ratio < 0.5) rendimiento += 30; else if (ratio < 0.75) rendimiento += 15;
        if (rep > 2) rendimiento += 20; else if (rep >= 1) rendimiento += 10;

        let compromiso = 0;
        if (asistencia < 50) compromiso += 50; else if (asistencia <= 70) compromiso += 30;
        if (moodle === "Nula (sin acceso)") compromiso += 50;
        else if (moodle.startsWith("Baja")) compromiso += 25;
        else if (moodle.startsWith("Media")) compromiso += 10;

        let socioeco = 0;
        if (e <= 1) socioeco += 30; else if (e <= 2) socioeco += 20; else if (e <= 3) socioeco += 10;
        if (trabaja && horasTrabajo > 30) socioeco += 30; else if (trabaja && horasTrabajo >= 15) socioeco += 15;
        if (!beca && e <= 2) socioeco += 20;
        if (dependientes) socioeco += 15;
        if (distancia === "> 2 horas") socioeco += 10;

        let bienestar = 0;
        if (estres > 7) bienestar += 40; else if (estres >= 5) bienestar += 20;
        if (faltasExamen === "Más de 3 veces") bienestar += 40;
        else if (faltasExamen === "2-3 veces") bienestar += 25;
        else if (faltasExamen === "1 vez") bienestar += 10;
        if (!psicologia && estres > 6) bienestar += 20;

        let apoyo = 0;
        if (likert[2] <= 2) apoyo += 40; else if (likert[2] === 3) apoyo += 20;
        if (likert[0] <= 2) apoyo += 35; else if (likert[0] === 3) apoyo += 15;
        if (likert[3] >= 4) apoyo += 25;

        return {
            rendimiento: Math.min(100, rendimiento),
            compromiso:  Math.min(100, compromiso),
            socioeco:    Math.min(100, socioeco),
            bienestar:   Math.min(100, bienestar),
            apoyo:       Math.min(100, apoyo),
        };
    });

    // ── Señales ──────────────────────────────────────────────────────────────
    const señales = $derived.by((): string[] => {
        if (!mostrarResultados) return [];
        const s: string[] = [];
        if (papa < 2.5) s.push(`P.A.P.A. de ${papa.toFixed(1)} por debajo del umbral crítico (2.5)`);
        else if (papa <= 3.2) s.push(`P.A.P.A. de ${papa.toFixed(1)} en zona de alerta (2.5–3.2)`);
        if (asistencia < 50) s.push(`Asistencia del ${asistencia}% (umbral crítico < 50%)`);
        else if (asistencia <= 70) s.push(`Asistencia del ${asistencia}% (por debajo del 70% recomendado)`);
        if (moodle === "Nula (sin acceso)") s.push("Sin acceso a plataforma virtual en las últimas 2 semanas");
        if (trabaja && horasTrabajo > 30) s.push(`Estrato ${estrato} trabajando ${horasTrabajo}h/semana (carga alta)`);
        else if (trabaja && horasTrabajo >= 15) s.push(`Trabaja ${horasTrabajo}h/semana en paralelo con estudios`);
        if (!beca && +estrato <= 2) s.push(`Estrato ${estrato} sin beca ni apoyo de bienestar`);
        if (estres > 7) s.push(`Nivel de estrés ${estres}/10 (nivel crítico)`);
        if (faltasExamen !== "Nunca") s.push(`${faltasExamen} de ausencias injustificadas en evaluaciones`);
        if (likert[3] >= 4) s.push("Pensamiento activo de cambio de carrera o universidad");
        return s.slice(0, 5);
    });

    // ── Intervención ─────────────────────────────────────────────────────────
    const intervencion = $derived.by(() => {
        if (!mostrarResultados || !factores) return null;
        const f = factores;
        const maxVal = Math.max(f.rendimiento, f.compromiso, f.socioeco, f.bienestar, f.apoyo);
        let tipo = "", icono = "", texto = "";
        if (maxVal === f.rendimiento || (maxVal === f.compromiso && f.rendimiento >= f.socioeco)) {
            tipo = "Tutoría Académica"; icono = "📚";
            texto = `Dado su P.A.P.A. de ${papa.toFixed(1)} y una asistencia del ${asistencia}%, se recomienda vinculación inmediata al programa de tutorías pares.`;
            if (moodle === "Nula (sin acceso)") texto += " La ausencia total en plataformas virtuales indica desconexión activa del proceso académico.";
        } else if (maxVal === f.bienestar) {
            tipo = "Atención Psicológica"; icono = "💚";
            texto = `Con un nivel de estrés de ${estres}/10${faltasExamen !== "Nunca" ? ` y ${faltasExamen.toLowerCase()} de ausencias injustificadas` : ""}, se recomienda orientación con Bienestar Universitario para acompañamiento emocional.`;
        } else if (maxVal === f.socioeco) {
            tipo = "Trabajo Social"; icono = "💼";
            texto = `El perfil socioeconómico (estrato ${estrato}${trabaja ? `, trabajando ${horasTrabajo}h/semana` : ""}${!beca ? ", sin apoyo de bienestar" : ""}) indica necesidad de gestión de apoyos económicos.`;
        } else {
            tipo = "Orientación y Acompañamiento"; icono = "🤝";
            texto = likert[3] >= 4
                ? "La intención de cambio de carrera sugiere necesidad de orientación vocacional y exploración de opciones dentro de la universidad."
                : "Se detecta debilitamiento en la red de apoyo personal. Se recomienda vinculación con grupos estudiantiles y mentoría.";
        }
        const prioridad = nivel === "alto" ? "Intervención inmediata" : nivel === "medio" ? "Seguimiento en 2 semanas" : "Monitoreo preventivo";
        return { tipo, icono, texto, prioridad };
    });

    // ── Colores ───────────────────────────────────────────────────────────────
    // Tres púrpuras distintos legibles sobre fondo #B069DB
    function nivelColor(n: string): string {
        return n === "alto"  ? "#1C0035" :   // morado muy oscuro
               n === "medio" ? "#9B27AF" :   // morado medio-oscuro saturado
                               "#E8C8FF";    // lavanda claro
    }

    function nivelLabel(n: string): string {
        return n === "alto" ? "RIESGO ALTO" : n === "medio" ? "RIESGO MEDIO" : "RIESGO BAJO";
    }

    function colorFactor(v: number): string {
        return v >= 66 ? "#1C0035" :   // morado muy oscuro
               v >= 36 ? "#9C27B0" :   // morado oscuro saturado
                         "#E1BEE7";    // lavanda claro
    }
</script>

<section class="alerta-temprana">
    <div class="alerta-header">
        <h2 class="titulo-ruta">CONSTRUCCIÓN DE RUTA DE TRABAJO</h2>
        <p class="subtexto">
            Formulario ampliado — factores académicos, socioeconómicos y de bienestar.
            Completa el perfil y presiona <strong>Analizar</strong> para ver el desglose.
        </p>
    </div>

    <!-- ══ CUADRÍCULA 2×2 ════════════════════════════════════════════════════ -->
    <div class="cuadricula">

        <!-- A: Datos Académicos -->
        <details class="seccion" open>
            <summary>A · Datos Académicos</summary>
            <div class="campo-grupo">
                <div class="campo">
                    <label>Promedio (P.A.P.A.): <strong>{papa.toFixed(1)}</strong></label>
                    <input type="range" min="0" max="5" step="0.1" bind:value={papa} />
                </div>
                <div class="campo creditos-fila">
                    <div class="credito-item">
                        <label>Aprobados</label>
                        <input type="number" min="0" max="20" bind:value={creditosAprobados} />
                    </div>
                    <div class="credito-item">
                        <label>Matriculados</label>
                        <input type="number" min="1" max="20" bind:value={creditosMatriculados} />
                    </div>
                </div>
                <div class="campo">
                    <label>Asistencia: <strong>{asistencia}%</strong></label>
                    <input type="range" min="0" max="100" step="5" bind:value={asistencia} />
                </div>
                <div class="campo">
                    <label>Materias reprobadas</label>
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
                    <label>Plataforma virtual (últ. 2 sem.)</label>
                    <select bind:value={moodle}>
                        <option>Alta ({">"}>5 accesos)</option>
                        <option>Media (2-5 accesos)</option>
                        <option>Baja (1-2 accesos)</option>
                        <option>Nula (sin acceso)</option>
                    </select>
                </div>
            </div>
        </details>

        <!-- B: Factores Socioeconómicos -->
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
                    <button type="button" class="toggle {trabaja ? 'activo' : ''}" onclick={() => trabaja = !trabaja}>
                        {trabaja ? "Sí" : "No"}
                    </button>
                </div>
                {#if trabaja}
                    <div class="campo" transition:slide={{ duration: 200 }}>
                        <label>Horas/semana: <strong>{horasTrabajo}h</strong></label>
                        <input type="range" min="0" max="60" step="1" bind:value={horasTrabajo} />
                    </div>
                {/if}
                <div class="campo fila-toggle">
                    <label>¿Recibe beca o apoyo?</label>
                    <button type="button" class="toggle {beca ? 'activo' : ''}" onclick={() => beca = !beca}>
                        {beca ? "Sí" : "No"}
                    </button>
                </div>
                <div class="campo fila-toggle">
                    <label>¿Tiene dependientes económicos?</label>
                    <button type="button" class="toggle {dependientes ? 'activo' : ''}" onclick={() => dependientes = !dependientes}>
                        {dependientes ? "Sí" : "No"}
                    </button>
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
                <img class="seccion-img" src={dinero} alt="Dinero" />
            </div>
        </details>

        <!-- C: Bienestar y Salud -->
        <details class="seccion" open>
            <summary>C · Bienestar y Salud</summary>
            <div class="campo-grupo">
                <div class="campo fila-toggle">
                    <label>¿Ha visitado psicología o bienestar?</label>
                    <button type="button" class="toggle {psicologia ? 'activo' : ''}" onclick={() => psicologia = !psicologia}>
                        {psicologia ? "Sí" : "No"}
                    </button>
                </div>
                <div class="campo">
                    <label>Nivel de estrés: <strong>{estres}/10</strong></label>
                    <input type="range" min="1" max="10" step="1" bind:value={estres} />
                    <span class="escala-hint">1 = muy bajo · 10 = muy alto</span>
                </div>
                <div class="campo">
                    <label>¿Ha faltado a exámenes sin justificación?</label>
                    <select bind:value={faltasExamen}>
                        <option>Nunca</option>
                        <option>1 vez</option>
                        <option>2-3 veces</option>
                        <option>Más de 3 veces</option>
                    </select>
                </div>
                <img class="seccion-img" src={loro} alt="Loro" />
            </div>
        </details>

        <!-- D: Cuestionario Likert -->
        <details class="seccion" open>
            <summary>D · Cuestionario Breve</summary>
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

    </div>

    <!-- ══ BOTONES ════════════════════════════════════════════════════════════ -->
    <div class="acciones">
        <button type="button" class="btn-random" onclick={randomizar}>
            🎲 Valores Aleatorios
        </button>
        <button type="button" class="btn-analizar" onclick={() => mostrarResultados = true}>
            🔍 Analizar Perfil de Riesgo
        </button>
    </div>

    <!-- ══ RESULTADOS (ancho completo, debajo) ══════════════════════════════ -->
    {#if !mostrarResultados}
        <div class="estado-vacio">
            <span class="vacio-icono">🎓</span>
            <p>Completa el perfil y presiona <strong>Analizar</strong> para ver el resultado.</p>
        </div>
    {:else}
        <div class="tarjeta-resultado" transition:fade={{ duration: 250 }}>

            <!-- Fila superior: badge + barra -->
            <div class="resultado-cabecera">
                <div class="nivel-badge" style="--col: {nivelColor(nivel)}">
                    <span class="nivel-texto">{nivelLabel(nivel)}</span>
                    <span class="nivel-puntaje">Puntuación: {puntaje} / 100</span>
                </div>
                <div class="barra-wrap">
                    <div class="barra-fondo">
                        <div class="barra-relleno" style="width: {puntaje}%; background: {nivelColor(nivel)}"></div>
                    </div>
                    <div class="barra-etiquetas">
                        <span>0</span><span>50</span><span>100</span>
                    </div>
                </div>
            </div>

            <!-- Cuerpo: dos columnas -->
            <div class="resultado-cuerpo">

                <!-- Izquierda: factores + señales -->
                <div class="resultado-col">
                    {#if factores}
                    <div class="bloque">
                        <h4>Factores de Riesgo</h4>
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
                                    <span style="color: {colorFactor(f.valor)}; font-weight:600">{f.valor}</span>
                                </div>
                                <div class="factor-barra-fondo">
                                    <div class="factor-barra-relleno" style="width:{f.valor}%; background:{colorFactor(f.valor)}"></div>
                                </div>
                            </div>
                        {/each}
                    </div>
                    {/if}
                </div>

                <!-- Derecha: intervención + señales -->
                <div class="resultado-col">
                    {#if intervencion}
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
                    <div class="bloque">
                        <h4>Señales Clave</h4>
                        <ul class="señales">
                            {#each señales as s}
                                <li>⚠ {s}</li>
                            {/each}
                        </ul>
                    </div>
                    {/if}
                </div>

            </div>

            <p class="disclaimer">
                Este análisis es generado por un modelo de demostración. En producción,
                el sistema utilizará datos reales del SIA y Moodle de la UNAL.
            </p>
        </div>
    {/if}

</section>

<style>
    /* ── Wrapper ──────────────────────────────────────────────────────────── */
    .alerta-temprana {
        margin-top: 2.5rem;
        padding-top: 2rem;
        border-top: 2px solid rgba(176, 105, 219, 0.3);
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .alerta-header {
        margin-bottom: 0.75rem;
    }

    .titulo-ruta {
        font-family: "Sekuya", serif;
        letter-spacing: 3px;
        font-size: 1.35rem;
        text-align: center;
        margin: 0 0 0.4rem;
    }

    .subtexto {
        font-size: 0.85rem;
        opacity: 0.65;
        margin: 0;
        text-align: center;
    }

    /* ── Cuadrícula 2×2 simétrica ───────────────────────────────────────── */
    .cuadricula {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        gap: 0.65rem;
        /* Las celdas de cada fila se estiran para igualar la altura */
        align-items: stretch;
    }

    @media (max-width: 600px) {
        .cuadricula { grid-template-columns: 1fr; grid-template-rows: none; }
    }

    /* ── Secciones ───────────────────────────────────────────────────────── */
    .seccion {
        background: #B069DB;
        color: #fff;
        border-radius: 0.75rem;
        overflow: hidden;
        /* Llena la celda del grid completamente */
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    .seccion > summary {
        padding: 0.65rem 1rem;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.88rem;
        list-style: none;
        user-select: none;
        display: flex;
        align-items: center;
        gap: 0.35rem;
        flex-shrink: 0;
    }

    .seccion > summary::before {
        content: "▸";
        display: inline-block;
        transition: transform 0.18s;
        font-size: 0.72rem;
        opacity: 0.65;
    }

    .seccion[open] > summary::before { transform: rotate(90deg); }

    /* ── Campos ──────────────────────────────────────────────────────────── */
    .campo-grupo {
        padding: 0.35rem 1rem 0.9rem;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        border-top: 1px solid rgba(255 255 255 / 0.15);
        /* Se expande para llenar el alto de la sección */
        flex: 1;
    }

    .campo { display: flex; flex-direction: column; gap: 0.2rem; }
    .campo label { font-size: 0.82rem; opacity: 0.9; }

    .campo.fila { flex-direction: row; gap: 0.6rem; }

    .sub-campo { flex: 1; display: flex; flex-direction: column; gap: 0.2rem; }

    /* Créditos: dos inputs pequeños centrados */
    .creditos-fila {
        flex-direction: row !important;
        justify-content: center;
        gap: 1.25rem;
    }

    .credito-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
    }

    .credito-item label { font-size: 0.78rem; opacity: 0.85; text-align: center; }

    .credito-item input[type="number"] {
        width: 3.5rem;
        text-align: center;
        background: rgba(255 255 255 / 0.15);
        color: #fff;
        border: 1px solid rgba(255 255 255 / 0.3);
        border-radius: 0.4rem;
        padding: 0.28rem 0.4rem;
        font-size: 0.88rem;
        font-family: inherit;
    }

    /* Imágenes de sección */
    .seccion-img {
        display: block;
        max-width: 80%;
        max-height: 130px;
        width: auto;
        height: auto;
        border-radius: 0.5rem;
        margin: auto auto 0;
        flex-shrink: 0;
    }

    .campo.fila-toggle {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
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
        padding: 0.28rem 0.4rem;
        font-size: 0.82rem;
        width: 100%;
        font-family: inherit;
    }

    .campo select {
        background: rgba(255 255 255 / 0.15);
        color: #fff;
        border: 1px solid rgba(255 255 255 / 0.3);
        border-radius: 0.4rem;
        padding: 0.28rem 0.4rem;
        font-size: 0.82rem;
        font-family: inherit;
        appearance: base-select;
    }

    .campo select option { background: Canvas; color: CanvasText; }

    .escala-hint { font-size: 0.7rem; opacity: 0.6; }

    /* ── Toggle ──────────────────────────────────────────────────────────── */
    .toggle {
        background: rgba(255 255 255 / 0.15);
        color: #fff;
        border: 1px solid rgba(255 255 255 / 0.35);
        border-radius: 1rem;
        padding: 0.18rem 0.7rem;
        font-size: 0.8rem;
        cursor: pointer;
        transition: background 0.15s;
        min-width: 3rem;
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

    /* ── Likert ──────────────────────────────────────────────────────────── */
    .likert-escala { font-size: 0.72rem; opacity: 0.6; margin: 0; }
    .likert-pregunta { margin-bottom: 0.35rem; }
    .likert-texto { font-size: 0.8rem; margin: 0 0 0.25rem; opacity: 0.95; }
    .likert-opciones { display: flex; gap: 0.5rem; }

    .likert-radio {
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
        gap: 0.08rem;
    }

    .likert-radio input[type="radio"] { accent-color: #fff; cursor: pointer; }
    .likert-num { font-size: 0.7rem; opacity: 0.75; }

    /* ── Botones ─────────────────────────────────────────────────────────── */
    .acciones {
        display: flex;
        gap: 0.65rem;
    }

    .btn-random {
        flex: 1;
        padding: 0.75rem;
        background: rgba(176, 105, 219, 0.15);
        color: #B069DB;
        border: 2px solid #B069DB;
        border-radius: 0.75rem;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.15s, color 0.15s;
        font-family: inherit;
    }

    .btn-random:hover {
        background: #B069DB;
        color: #fff;
    }

    .btn-analizar {
        flex: 2;
        padding: 0.75rem;
        background: #7B3ABF;
        color: #fff;
        border: none;
        border-radius: 0.75rem;
        font-size: 0.95rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.15s;
        font-family: inherit;
    }

    .btn-analizar:hover { background: #6A2FA8; }

    /* ── Estado vacío ────────────────────────────────────────────────────── */
    .estado-vacio {
        background: rgba(176, 105, 219, 0.07);
        border: 2px dashed rgba(176, 105, 219, 0.3);
        border-radius: 0.75rem;
        padding: 2.5rem 1.5rem;
        text-align: center;
        opacity: 0.7;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.6rem;
    }

    .vacio-icono { font-size: 2.2rem; }

    /* ── Tarjeta resultado ───────────────────────────────────────────────── */
    .tarjeta-resultado {
        background: #B069DB;
        color: #fff;
        border-radius: 0.75rem;
        padding: 1.25rem 1.4rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    /* Cabecera: badge + barra side-by-side */
    .resultado-cabecera {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    @media (max-width: 500px) {
        .resultado-cabecera { flex-direction: column; align-items: stretch; }
    }

    /* Badge de nivel — tres púrpuras distintos */
    .nivel-badge {
        text-align: center;
        background: rgba(255 255 255 / 0.12);
        border: 2px solid var(--col);
        border-radius: 0.6rem;
        padding: 0.7rem 1.2rem;
        flex-shrink: 0;
    }

    .nivel-texto {
        display: block;
        font-size: 1.2rem;
        font-weight: 700;
        font-family: "Sekuya", serif;
        letter-spacing: 1px;
        color: var(--col);
        text-shadow: 0 1px 4px rgba(255 255 255 / 0.2);
    }

    .nivel-puntaje {
        display: block;
        font-size: 0.82rem;
        opacity: 0.8;
        margin-top: 0.25rem;
    }

    /* Barra de puntaje */
    .barra-wrap { flex: 1; display: flex; flex-direction: column; gap: 0.25rem; }

    .barra-fondo {
        background: rgba(255 255 255 / 0.2);
        border-radius: 1rem;
        height: 0.65rem;
        overflow: hidden;
    }

    .barra-relleno {
        height: 100%;
        border-radius: 1rem;
        transition: width 0.4s ease;
        min-width: 0.3rem;
    }

    .barra-etiquetas {
        display: flex;
        justify-content: space-between;
        font-size: 0.68rem;
        opacity: 0.55;
    }

    /* Cuerpo dos columnas */
    .resultado-cuerpo {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        align-items: start;
    }

    @media (max-width: 500px) {
        .resultado-cuerpo { grid-template-columns: 1fr; }
    }

    .resultado-col { display: flex; flex-direction: column; gap: 0.9rem; }

    /* Bloques */
    .bloque { display: flex; flex-direction: column; gap: 0.45rem; }

    .bloque h4 {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.6;
        margin: 0;
    }

    /* Barras de factores */
    .factor { display: flex; flex-direction: column; gap: 0.18rem; }

    .factor-cabecera {
        display: flex;
        justify-content: space-between;
        font-size: 0.78rem;
        opacity: 0.9;
    }

    .factor-barra-fondo {
        background: rgba(255 255 255 / 0.2);
        border-radius: 1rem;
        height: 0.38rem;
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
        border-radius: 0.5rem;
        padding: 0.7rem 0.85rem;
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }

    .intervencion-tipo { display: flex; align-items: center; gap: 0.4rem; }
    .intervencion-icono { font-size: 1.1rem; }
    .intervencion-nombre { font-weight: 600; font-size: 0.88rem; }

    .intervencion-texto {
        font-size: 0.8rem;
        line-height: 1.5;
        opacity: 0.9;
        margin: 0;
    }

    .prioridad {
        display: inline-block;
        background: rgba(255 255 255 / 0.18);
        border-radius: 1rem;
        padding: 0.15rem 0.6rem;
        font-size: 0.74rem;
        font-weight: 600;
        align-self: flex-start;
    }

    /* Señales clave: dos por fila */
    .señales {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.3rem 0.75rem;
    }

    .señales li {
        font-size: 0.76rem;
        opacity: 0.87;
        padding: 0.3rem 0.5rem;
        border-radius: 0.35rem;
        background: rgba(255 255 255 / 0.1);
        line-height: 1.4;
    }

    @media (max-width: 500px) {
        .señales { grid-template-columns: 1fr; }
    }

    /* Disclaimer */
    .disclaimer {
        font-size: 0.68rem;
        opacity: 0.4;
        text-align: center;
        margin: 0;
        line-height: 1.5;
    }
</style>
