<script lang="ts">
	import { fade, slide } from 'svelte/transition';

	let riskPool = $state(58);
	let mlPrecision = $state(80);
	let acceptanceRate = $state(60);
	let successRate = $state(39);
	let isExpanded = $state(false);

	const BASE = 6240;

	const SALARIO_PSICOLOGO = 4_817_000;
	const SALARIO_TUTOR = 1_824_000;
	const SALARIO_TRAB_SOCIAL = 3_200_000;
	const LICENCIAS_MENSUAL = 1_926_000;
	const LICENCIAS_ANUAL = 23_112_000;
	const MANTENIMIENTO_MENSUAL = 2_857_000;
	const MANTENIMIENTO_ANUAL = 34_284_000;
	const OPEX_FIJO_ANUAL = LICENCIAS_ANUAL + MANTENIMIENTO_ANUAL;
	const CAPEX_INGENIEROS = 24_000_000;
	const CAPEX_ASESOR = 4_500_000;
	const CAPEX_TOTAL = 38_778_000;

	const URL_UNAL_REMUN = 'https://personal.manizales.unal.edu.co/fileadmin/user_upload/REMUNERACION-PLANTA-ADMINISTRATIVA-VIGENCIA-2020.pdf';
	const URL_AUX_UNAL = 'https://1drv.ms/b/c/e020114ca07d2683/IQA3Kuj54veiT53xXB7suYNbAWEIxK4rmQbtgkA?e=rTDXHH';
	const URL_FORMATO_AUX = 'https://drive.google.com/file/d/1EeXua7gSvT5Pp1MxtEBrGonKPyvtMCn0/view?usp=drive_link';
	const URL_INDEED = 'https://co.indeed.com/career/trabajadora-social/salaries';
	const URL_ORACLE = 'https://www.oracle.com/latam/cloud/pricing/';
	const URL_UCC = 'https://repository.ucc.edu.co/server/api/core/bitstreams/bcb6ecca-4377-4cd9-918c-843fc396d8dd/content';

	type Marker = {
		v: number;
		tag: string;
		tooltip: string;
		link?: string;
		isBase?: boolean;
	};

	const MARKERS_S1: Marker[] = [
		{
			v: 53,
			tag: 'ScienceDirect',
			tooltip:
				'Predicting student dropouts with ML – ScienceDirect 2024. Recall 53.2–54.1% en modelo de deserción residencial universitaria.',
			link: 'https://www.sciencedirect.com/science/article/pii/S0160791X24000228'
		},
		{
			v: 58,
			tag: 'UNAL base',
			tooltip: 'Supuesto propio – pendiente de validación piloto',
			isBase: true
		},
		{
			v: 70,
			tag: 'arXiv 2024',
			tooltip:
				'Early Detection of At-Risk Students Using ML – arXiv 2024 (CalState Fullerton). Recall hasta 70% con datos LMS + rendimiento académico.',
			link: 'https://arxiv.org/abs/2412.09483'
		}
	];

	const MARKERS_S2: Marker[] = [
		{
			v: 78,
			tag: 'Nature 2025',
			tooltip:
				'Student dropout prediction through ML – Nature Scientific Reports 2025. Precision 78–86% en múltiples modelos universitarios.',
			link: 'https://www.nature.com/articles/s41598-025-93918-1'
		},
		{
			v: 80,
			tag: 'UNAL base',
			tooltip: 'Supuesto propio – pendiente de validación piloto',
			isBase: true
		},
		{
			v: 84,
			tag: 'ScienceDirect',
			tooltip:
				'Predicting student dropouts with ML – ScienceDirect 2024. Precision 83.6–83.9% en modelo supervisado.',
			link: 'https://www.sciencedirect.com/science/article/pii/S0160791X24000228'
		}
	];

	const MARKERS_S3: Marker[] = [
		{
			v: 50,
			tag: 'Mohawk',
			tooltip:
				'Proactive Advising Retention Outcomes Report – Mohawk College. Tasas de participación en outreach proactivo entre 50–70% según modalidad de contacto.',
			link: 'https://www.mohawkcollege.ca/sites/default/files/accessible-pdf/cssic/Proactive%20Advising%20Retention%20Outcomes%20Report.%20FINAL.pdf'
		},
		{
			v: 60,
			tag: 'UNAL base',
			tooltip: 'Supuesto propio – pendiente de validación piloto',
			isBase: true
		},
		{
			v: 65,
			tag: 'HEQCO 2017',
			tooltip:
				'Academic Advising: Measuring the Effects of Proactive Interventions – HEQCO Canadá 2017. El 65% de estudiantes en riesgo aceptó participar en sesiones de advising grupal.',
			link: 'https://heqco.ca/pub/academic-advising-measuring-the-effects-of-proactive-interventions-on-student-outcomes/'
		}
	];

	const MARKERS_S4: Marker[] = [
		{
			v: 38,
			tag: 'J.Soc.Work',
			tooltip:
				'Dropout Prevention and Intervention Programs – Journal of Social Work Research 2013 (152 estudios). Tasa de deserción redujo de 21.1% a 13% en grupo de intervención (~38% de casos evitables resueltos).',
			link: 'https://www.journals.uchicago.edu/doi/abs/10.5243/jsswr.2013.22'
		},
		{
			v: 40,
			tag: 'Civitas',
			tooltip:
				'Effective Academic Advising Strategies – Civitas Learning 2021 (55 universidades). El advising aumentó la retención en +6.36 puntos porcentuales en universidades de 4 años.',
			link: 'https://www.civitaslearning.com/blog/effective-academic-advising-strategies/'
		},
		{
			v: 39,
			tag: 'UNAL base',
			tooltip: 'Supuesto propio — pendiente de validación piloto en la UNAL.',
			isBase: true
		}
	];

	function pos(v: number, min: number, max: number): number {
		return ((v - min) / (max - min)) * 100;
	}

	let step1 = $derived(Math.round(BASE * (riskPool / 100) * (mlPrecision / 100)));
	let step2 = $derived(Math.round(step1 * (acceptanceRate / 100)));
	let step3 = $derived(Math.round(step2 * (successRate / 100) * 0.68));
	let savingsM = $derived(parseFloat((step3 * 19.5).toFixed(1)));

	let nPsicologos = $derived(Math.ceil((step2 * 0.20) / 100));
	let nTutores = $derived(Math.ceil((step2 * 0.25) / 10));
	let nTrabSoc = $derived(Math.ceil((step2 * 0.30) / 100));

	let mensualPsicologos = $derived(nPsicologos * SALARIO_PSICOLOGO);
	let mensualTutores = $derived(nTutores * SALARIO_TUTOR);
	let mensualTrabSoc = $derived(nTrabSoc * SALARIO_TRAB_SOCIAL);
	let anualPsicologos = $derived(mensualPsicologos * 12);
	let anualTutores = $derived(mensualTutores * 12);
	let anualTrabSoc = $derived(mensualTrabSoc * 12);

	let costoVariableAnual = $derived(anualPsicologos + anualTutores + anualTrabSoc);
	let costoTotalAnual = $derived(costoVariableAnual + OPEX_FIJO_ANUAL);

	let costM = $derived(parseFloat((costoTotalAnual / 1_000_000).toFixed(1)));
	let balanceM = $derived(parseFloat((savingsM - costM).toFixed(1)));

	function fmt(n: number): string {
		return n.toLocaleString('es-CO');
	}
</script>

<div class="pres" transition:fade={{ duration: 150 }}>

	<!-- ══════════════════════════════════════════
	     HERO
	══════════════════════════════════════════ -->
	<section class="hero">
		<div class="wrap">
			<p class="eyebrow">Sistema de Alerta Temprana IA – UNAL Bogotá</p>
			<h2>Reducción de la Deserción Estudiantil con I.A.</h2>
			<p class="hero-sub">Universidad Nacional de Colombia · Sede Bogotá</p>
			<p class="hero-body">
				Cada año, aproximadamente 6.240 estudiantes abandonan sus estudios en la UNAL Bogotá.
				Este proyecto propone un sistema de alerta temprana basado en IA que identifica
				estudiantes en riesgo y los conecta con el especialista adecuado — antes de que deserten.
			</p>
		</div>
	</section>

	<!-- ══════════════════════════════════════════
	     EL PROBLEMA
	══════════════════════════════════════════ -->
	<section class="problem">
		<div class="wrap">
			<h2 class="stitle">El Problema</h2>
			<div class="stat-grid">
				<article class="stat-card">
					<span class="stat-n">12.4%</span>
					<span class="stat-d">Tasa anual de deserción en Colombia</span>
					<span class="stat-s">SPADIES 2023</span>
				</article>
				<article class="stat-card">
					<span class="stat-n">22%</span>
					<span class="stat-d">Estudiantes que abandonan en el primer año</span>
					<span class="stat-s">OCDE 2025</span>
				</article>
				<article class="stat-card">
					<span class="stat-n">6.240</span>
					<span class="stat-d">Deserciones estimadas por año en UNAL Bogotá</span>
					<span class="stat-s">Estimación interna</span>
				</article>
			</div>
			<p class="note">
				Cada deserción representa una pérdida estatal de aprox.
				<strong>19,5 millones de COP</strong>.
			</p>
		</div>
	</section>

	<!-- ══════════════════════════════════════════
	     SIMULADOR
	══════════════════════════════════════════ -->
	<section class="sim" id="simulador">
		<div class="wrap">
			<h2 class="stitle on-dark">Simulador del Modelo de Intervención</h2>
			<p class="stitle-sub">Ajusta los parámetros y observa el impacto en tiempo real</p>

			<div class="sim-grid">
				<!-- Embudo de pasos -->
				<div class="funnel">
					<div class="fstep fs1">
						<span class="fl">Desertores identificables</span>
						<span class="fv">{fmt(step1)}</span>
						<span class="fu">estudiantes</span>
					</div>
					<span class="farr">▼</span>
					<div class="fstep fs2">
						<span class="fl">Aceptan el apoyo</span>
						<span class="fv">{fmt(step2)}</span>
						<span class="fu">estudiantes</span>
					</div>
					<span class="farr">▼</span>
					<div class="fstep fs3">
						<span class="fl">Deserción prevenida</span>
						<span class="fv">{fmt(step3)}</span>
						<span class="fu">estudiantes</span>
					</div>
					<span class="farr">▼</span>
					<div class="fstep fs4">
						<span class="fl">Ahorro para la UNAL</span>
						<span class="fv">{fmt(savingsM)}</span>
						<span class="fu">millones COP</span>
					</div>
				</div>

				<!-- Panel de sliders -->
				<div class="sliders">
					{#snippet markerLayer(markers: Marker[], min: number, max: number)}
						<div class="markers">
							{#each markers as m (m.v)}
								{@const p = pos(m.v, min, max)}
								<div
									class="marker"
									class:m-base={m.isBase}
									class:edge-left={p < 18}
									class:edge-right={p > 82}
									style="left: {p}%"
									tabindex="0"
									role="button"
									aria-label="{m.tag} {m.v}%: {m.tooltip}"
								>
									<span class="tick" aria-hidden="true"></span>
									<span class="m-content">
										<span class="m-val">{m.v}%</span>
										<span class="m-tag">{m.tag}</span>
									</span>
									<span class="m-tooltip" role="tooltip">
										<span class="mt-body">{m.tooltip}</span>
										{#if m.link}
											<a
												class="mt-link"
												href={m.link}
												target="_blank"
												rel="noopener noreferrer"
											>
												→ Ver fuente
											</a>
										{/if}
									</span>
								</div>
							{/each}
						</div>
					{/snippet}

					<div class="srow">
						<div class="slbl">
							<span>Tasa de identificación ML</span>
							<span class="sv">{riskPool}%</span>
						</div>
						<div class="track-wrap">
							<input type="range" min="10" max="90" step="1" bind:value={riskPool} />
							{@render markerLayer(MARKERS_S1, 10, 90)}
						</div>
					</div>
					<div class="srow">
						<div class="slbl">
							<span>Precisión del modelo ML</span>
							<span class="sv">{mlPrecision}%</span>
						</div>
						<div class="track-wrap">
							<input type="range" min="50" max="95" step="1" bind:value={mlPrecision} />
							{@render markerLayer(MARKERS_S2, 50, 95)}
						</div>
					</div>
					<div class="srow">
						<div class="slbl">
							<span>Tasa de aceptación del apoyo</span>
							<span class="sv">{acceptanceRate}%</span>
						</div>
						<div class="track-wrap">
							<input type="range" min="20" max="80" step="1" bind:value={acceptanceRate} />
							{@render markerLayer(MARKERS_S3, 20, 80)}
						</div>
					</div>
					<div class="srow">
						<div class="slbl">
							<span>Tasa de éxito de la intervención</span>
							<span class="sv">{successRate}%</span>
						</div>
						<div class="track-wrap">
							<input type="range" min="20" max="70" step="1" bind:value={successRate} />
							{@render markerLayer(MARKERS_S4, 20, 70)}
						</div>
					</div>
				</div>
			</div>

			<!-- Métricas financieras -->
			<div class="metrics">
				<div class="metric msav">
					<span class="ml">Pérdidas prevenidas (anual)</span>
					<span class="mv">{fmt(savingsM)} M COP</span>
				</div>
				<div class="metric mcost">
					<span class="ml">Costo del sistema (anual)</span>
					<span class="mv">{fmt(costM)} M COP</span>
				</div>
				<div class="metric mbal" class:pos={balanceM >= 0} class:neg={balanceM < 0}>
					<span class="ml">Balance neto</span>
					<span class="mv">{fmt(balanceM)} M COP</span>
				</div>
			</div>

			<p class="capex-note">
				Inversión inicial (año 0): {fmt(CAPEX_TOTAL)} COP
			</p>

			<button class="expand-btn" onclick={() => (isExpanded = !isExpanded)}>
				{isExpanded ? '▼ Ocultar desglose' : '▶️ Ver desglose detallado de costos'}
			</button>

			{#if isExpanded}
				<div class="breakdown" transition:slide={{ duration: 280 }}>
					<!-- ── Personal de Intervención ───────────── -->
					<div class="sub sub-personal">
						<h3 class="sub-title">Personal de Intervención</h3>

						<!-- Psicólogos -->
						<div class="row" style="--accent: #7C3AED">
							<div class="row-head">
								<span class="row-icon">🧠</span>
								<div class="row-text">
									<strong>Psicólogos de Bienestar</strong>
									<span class="row-desc">1 psicólogo por cada 100 estudiantes · salud mental</span>
								</div>
								<div class="row-amounts">
									<span class="amount-annual">{fmt(anualPsicologos)} COP/año</span>
									<span class="amount-monthly">{fmt(nPsicologos)} × {fmt(SALARIO_PSICOLOGO)} COP/mes</span>
								</div>
							</div>
							<a class="src-link" href={URL_UNAL_REMUN} target="_blank" rel="noopener noreferrer">
								Remuneración planta UNAL 2020 →
							</a>
						</div>

						<!-- Tutores Pares -->
						<div class="row" style="--accent: #2563EB">
							<div class="row-head">
								<span class="row-icon">📚</span>
								<div class="row-text">
									<strong>Tutores Pares</strong>
									<span class="row-desc">1 tutor por cada 10 estudiantes · 20h semanales · apoyo académico</span>
								</div>
								<div class="row-amounts">
									<span class="amount-annual">{fmt(anualTutores)} COP/año</span>
									<span class="amount-monthly">{fmt(nTutores)} × {fmt(SALARIO_TUTOR)} COP/mes</span>
								</div>
							</div>
							<a class="src-link" href={URL_AUX_UNAL} target="_blank" rel="noopener noreferrer">
								Convocatoria auxiliares UNAL 2025 →
							</a>
						</div>

						<!-- Trabajadores Sociales -->
						<div class="row" style="--accent: #059669">
							<div class="row-head">
								<span class="row-icon">🤝</span>
								<div class="row-text">
									<strong>Trabajadores Sociales</strong>
									<span class="row-desc">1 trabajador social por cada 100 estudiantes · vulnerabilidad socioeconómica</span>
								</div>
								<div class="row-amounts">
									<span class="amount-annual">{fmt(anualTrabSoc)} COP/año</span>
									<span class="amount-monthly">
										{fmt(nTrabSoc)} × {fmt(SALARIO_TRAB_SOCIAL)} COP/mes<span class="tooltip-wrap">
											<span class="info-icon" tabindex="0" role="button" aria-label="¿Por qué 3.200.000 COP?">ⓘ</span>
											<span class="tooltip-card" role="tooltip">
												<strong class="tt-title">¿Por qué 3.200.000 COP?</strong>
												El salario base promedio según Indeed Colombia es de 2.460.459 COP/mes. El valor usado en el modelo (3.200.000 COP) incluye prestaciones sociales obligatorias (~47%): cesantías, prima, vacaciones, salud, pensión y ARL. Costo real al empleador = salario base × 1,47.
												<a class="tt-link" href={URL_INDEED} target="_blank" rel="noopener noreferrer">Ver referencia Indeed →</a>
											</span>
										</span>
									</span>
								</div>
							</div>
							<a class="src-link" href={URL_INDEED} target="_blank" rel="noopener noreferrer">
								Salarios Indeed Colombia →
							</a>
						</div>
					</div>

					<!-- ── Costos Fijos del Sistema ───────────── -->
					<div class="sub sub-fijos">
						<h3 class="sub-title">Costos Fijos del Sistema</h3>

						<!-- Ingenieros de Sistemas -->
						<div class="row row-fixed">
							<div class="row-head">
								<span class="row-icon">💻</span>
								<div class="row-text">
									<strong>Ingenieros de Sistemas (×2)</strong>
									<span class="row-desc">2 ingenieros · tiempo completo · 3 meses · desarrollo del modelo</span>
									<span class="badge badge-once">Inversión única</span>
								</div>
								<div class="row-amounts">
									<span class="amount-annual">{fmt(CAPEX_INGENIEROS)} COP</span>
								</div>
							</div>
							<a class="src-link" href={URL_UNAL_REMUN} target="_blank" rel="noopener noreferrer">
								Remuneración planta UNAL 2020 →
							</a>
						</div>

						<!-- Asesor Especializado -->
						<div class="row row-fixed">
							<div class="row-head">
								<span class="row-icon">🧑‍🏫</span>
								<div class="row-text">
									<strong>Asesor Especializado</strong>
									<span class="row-desc">Psicólogo · medio tiempo · 3 meses · variables de riesgo</span>
									<span class="badge badge-once">Inversión única</span>
								</div>
								<div class="row-amounts">
									<span class="amount-annual">{fmt(CAPEX_ASESOR)} COP</span>
									<span class="amount-monthly">incluida en CAPEX</span>
								</div>
							</div>
							<a class="src-link" href={URL_FORMATO_AUX} target="_blank" rel="noopener noreferrer">
								Formato auxiliares UNAL 2025 →
							</a>
						</div>

						<!-- Licencias Tecnológicas -->
						<div class="row row-fixed">
							<div class="row-head">
								<span class="row-icon">☁️</span>
								<div class="row-text">
									<strong>Licencias Tecnológicas</strong>
									<span class="row-desc">Oracle ADF, Java EE, servicios en la nube</span>
									<span class="badge badge-recurring">Costo recurrente</span>
								</div>
								<div class="row-amounts">
									<span class="amount-annual">{fmt(LICENCIAS_ANUAL)} COP/año</span>
									<span class="amount-monthly">{fmt(LICENCIAS_MENSUAL)} COP/mes</span>
								</div>
							</div>
							<a class="src-link" href={URL_ORACLE} target="_blank" rel="noopener noreferrer">
								Oracle Cloud Pricing LATAM →
							</a>
						</div>

						<!-- Mantenimiento Técnico -->
						<div class="row row-fixed">
							<div class="row-head">
								<span class="row-icon">🔧</span>
								<div class="row-text">
									<strong>Mantenimiento Técnico</strong>
									<span class="row-desc">Ingeniero de soporte · medio tiempo · mantenimiento continuo</span>
									<span class="badge badge-recurring">Costo recurrente</span>
								</div>
								<div class="row-amounts">
									<span class="amount-annual">{fmt(MANTENIMIENTO_ANUAL)} COP/año</span>
									<span class="amount-monthly">{fmt(MANTENIMIENTO_MENSUAL)} COP/mes</span>
								</div>
							</div>
							<a class="src-link" href={URL_UCC} target="_blank" rel="noopener noreferrer">
								Referencia salarial UCC →
							</a>
						</div>
					</div>

					<p class="footnote">
						Fuentes:
						<a href={URL_UNAL_REMUN} target="_blank" rel="noopener noreferrer">Remuneración UNAL Manizales 2020</a> ·
						<a href={URL_AUX_UNAL} target="_blank" rel="noopener noreferrer">Convocatoria auxiliares UNAL 2025</a> ·
						<a href={URL_ORACLE} target="_blank" rel="noopener noreferrer">Oracle Cloud Pricing</a> ·
						<a href={URL_INDEED} target="_blank" rel="noopener noreferrer">Indeed Colombia</a> ·
						SPADIES 2023
					</p>
				</div>
			{/if}
		</div>
	</section>

	<!-- ══════════════════════════════════════════
	     POR QUÉ FUNCIONA
	══════════════════════════════════════════ -->
	<section class="why">
		<div class="wrap">
			<h2 class="stitle">¿Por qué funciona?</h2>
			<div class="why-grid">
				<div class="why-card">
					<h3>Evidencia Internacional</h3>
					<p>
						Georgia State University incrementó sus tasas de graduación en un 5% usando un
						sistema similar. El programa BID FAIR-LAC documentó la alerta temprana con IA como
						práctica óptima para universidades latinoamericanas.
					</p>
				</div>
				<div class="why-card">
					<h3>El Modelo</h3>
					<p>
						El sistema no reemplaza a los especialistas humanos — garantiza que los recursos
						limitados de acompañamiento lleguen a los estudiantes que más los necesitan,
						en el momento oportuno.
					</p>
				</div>
				<div class="why-card">
					<h3>Próximos pasos</h3>
					<p>
						<strong>Fase 1:</strong> Piloto de datos (Semestre 1)<br />
						<strong>Fase 2:</strong> Piloto de facultad con calibración empírica<br />
						<strong>Fase 3:</strong> Despliegue completo en UNAL Bogotá<br />
						<strong>Fase 4:</strong> Evaluación y escalado a otras sedes
					</p>
				</div>
			</div>
		</div>
	</section>

	<!-- ══════════════════════════════════════════
	     FOOTER
	══════════════════════════════════════════ -->
	<footer>
		<p>
			Proyecto de investigación – UNAL Bogotá · 2026 · Estudio de Factibilidad Económica:
			Sistema de Alerta Temprana Basado en IA
		</p>
	</footer>
</div>

<style>
	/* ── Escape del contenedor 800px ─────────────────────────────── */
	:global(html) {
		overflow-x: clip;
	}

	.pres {
		/* Breaks out of the 800px body container to fill html width */
		width: calc(100vw - 40px);
		margin-left: calc(-50vw + 50% + 20px);
	}

	/* ── Contenedor interior centrado ────────────────────────────── */
	.wrap {
		max-width: 1080px;
		margin: 0 auto;
		padding: 4rem 2rem;
	}

	/* ── Tipografía compartida ───────────────────────────────────── */
	h2,
	h3 {
		font-family: 'Sekuya', serif;
		letter-spacing: 3px;
		line-height: 1.2;
		margin: 0;
	}

	.stitle {
		font-size: clamp(1.5rem, 3vw, 2.2rem);
		text-align: center;
		margin-bottom: 0.5rem;
		color: oklch(0.22 0.18 304);
	}

	.stitle.on-dark {
		color: #fff;
	}

	.stitle-sub {
		text-align: center;
		color: rgba(255, 255, 255, 0.7);
		margin: 0 0 2.5rem 0;
		font-size: 1rem;
	}

	/* ── HERO ────────────────────────────────────────────────────── */
	.hero {
		background: linear-gradient(
			140deg,
			oklch(0.16 0.18 310) 0%,
			oklch(0.26 0.22 304) 55%,
			oklch(0.2 0.14 292) 100%
		);
		color: #fff;
	}

	.hero .wrap {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		gap: 1.2rem;
		padding-top: 5rem;
		padding-bottom: 5.5rem;
	}

	.eyebrow {
		font-size: 0.78rem;
		font-weight: 700;
		letter-spacing: 2.5px;
		text-transform: uppercase;
		color: oklch(0.82 0.18 304);
		margin: 0;
	}

	.hero h2 {
		font-size: clamp(1.4rem, 3vw, 2rem);
		color: #fff;
		max-width: 820px;
	}

	.hero-sub {
		font-size: 0.95rem;
		opacity: 0.65;
		margin: 0;
		letter-spacing: 1px;
	}

	.hero-body {
		font-size: 1.05rem;
		line-height: 1.75;
		opacity: 0.88;
		max-width: 640px;
		margin: 0;
	}

	.cta {
		display: inline-block;
		margin-top: 0.4rem;
		padding: 0.85rem 2.4rem;
		background: oklch(0.58 0.26 304);
		color: #fff;
		border-radius: 9999px;
		text-decoration: none;
		font-weight: 700;
		font-size: 0.95rem;
		letter-spacing: 1px;
		transition:
			background 0.2s,
			transform 0.15s;
	}

	.cta:hover {
		background: oklch(0.68 0.26 304);
		transform: translateY(-2px);
	}

	/* ── EL PROBLEMA ─────────────────────────────────────────────── */
	.problem {
		background: #fff;
	}

	.problem .wrap {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 2rem;
	}

	.stat-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 1.25rem;
		width: 100%;
	}

	.stat-card {
		background: linear-gradient(
			140deg,
			oklch(0.44 0.23 304),
			oklch(0.37 0.18 308)
		);
		border-radius: 1rem;
		padding: 2rem 1.5rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		gap: 0.45rem;
		box-shadow: 0 6px 24px oklch(0.44 0.23 304 / 0.32);
		color: #fff;
	}

	.stat-n {
		font-family: 'Sekuya', serif;
		font-size: clamp(2rem, 5vw, 2.8rem);
		letter-spacing: 2px;
		line-height: 1;
	}

	.stat-d {
		font-size: 0.88rem;
		opacity: 0.9;
		line-height: 1.45;
	}

	.stat-s {
		font-size: 0.72rem;
		opacity: 0.55;
		font-style: italic;
	}

	.note {
		text-align: center;
		font-size: 1rem;
		color: oklch(0.32 0.1 304);
		max-width: 560px;
		margin: 0;
		line-height: 1.6;
	}

	/* ── SIMULADOR ───────────────────────────────────────────────── */
	.sim {
		background: linear-gradient(
			160deg,
			oklch(0.24 0.2 308) 0%,
			oklch(0.33 0.18 300) 100%
		);
		color: #fff;
	}

	.sim .wrap {
		display: flex;
		flex-direction: column;
	}

	.sim-grid {
		display: grid;
		grid-template-columns: 1fr 1.5fr;
		gap: 2.5rem;
		align-items: start;
		margin-bottom: 2.5rem;
	}

	@media (max-width: 680px) {
		.sim-grid {
			grid-template-columns: 1fr;
		}
	}

	/* Embudo */
	.funnel {
		display: flex;
		flex-direction: column;
		align-items: stretch;
		gap: 0;
	}

	.fstep {
		border-radius: 0.7rem;
		padding: 1.1rem 1.25rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		transition:
			background 0.3s ease,
			box-shadow 0.3s ease;
	}

	.fl {
		font-size: 0.72rem;
		text-transform: uppercase;
		letter-spacing: 1.2px;
		opacity: 0.78;
		margin-bottom: 0.2rem;
	}

	.fv {
		font-family: 'Sekuya', serif;
		font-size: clamp(1.4rem, 2.8vw, 1.9rem);
		letter-spacing: 2px;
		line-height: 1.1;
		transition: all 0.3s ease;
	}

	.fu {
		font-size: 0.7rem;
		opacity: 0.62;
		margin-top: 0.1rem;
	}

	.fs1 {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.18);
	}

	.fs2 {
		background: oklch(0.4 0.2 284);
		box-shadow: 0 3px 14px oklch(0.4 0.2 284 / 0.4);
	}

	.fs3 {
		background: oklch(0.44 0.23 304);
		box-shadow: 0 3px 14px oklch(0.44 0.23 304 / 0.4);
	}

	.fs4 {
		background: oklch(0.35 0.2 312);
		box-shadow: 0 3px 14px oklch(0.35 0.2 312 / 0.4);
	}

	.farr {
		text-align: center;
		font-size: 1rem;
		opacity: 0.4;
		padding: 0.12rem 0;
		display: block;
	}

	/* Sliders */
	.sliders {
		display: flex;
		flex-direction: column;
		gap: 2.25rem;
		padding: 1.85rem 1.75rem 1.5rem;
		background: rgba(255, 255, 255, 0.07);
		border-radius: 1rem;
		border: 1px solid rgba(255, 255, 255, 0.12);
	}

	.srow {
		display: flex;
		flex-direction: column;
		gap: 0.15rem;
		min-height: 80px;
	}

	.slbl {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.88rem;
	}

	.sv {
		font-family: 'Sekuya', serif;
		font-size: 1.05rem;
		letter-spacing: 1px;
		color: oklch(0.84 0.2 304);
		min-width: 3rem;
		text-align: right;
	}

	.track-wrap {
		position: relative;
		padding-bottom: 44px;
	}

	input[type='range'] {
		width: 100%;
		accent-color: oklch(0.68 0.26 304);
		cursor: pointer;
		height: 5px;
		display: block;
		position: relative;
		z-index: 2;
	}

	/* ── Capa de marcadores de referencia ────────────────────────── */
	.markers {
		position: absolute;
		top: calc(100% + 6px);
		left: 0;
		right: 0;
		height: 0;
		pointer-events: none;
		z-index: 1;
	}

	.marker {
		position: absolute;
		top: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		transform: translateX(-50%);
		pointer-events: auto;
		cursor: help;
		outline: none;
		min-width: 24px;
	}

	.tick {
		width: 1.5px;
		height: 7px;
		background: rgba(255, 255, 255, 0.45);
		display: block;
		pointer-events: none;
	}

	.m-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-top: 2px;
		line-height: 1.1;
	}

	.m-val {
		font-size: 10px;
		font-weight: 700;
		color: rgba(255, 255, 255, 0.78);
		font-variant-numeric: tabular-nums;
		letter-spacing: 0.2px;
	}

	.m-tag {
		font-size: 8.5px;
		color: rgba(255, 255, 255, 0.5);
		margin-top: 1px;
		white-space: nowrap;
		letter-spacing: 0.15px;
	}

	.marker:hover .m-val,
	.marker:hover .m-tag,
	.marker:focus-visible .m-val,
	.marker:focus-visible .m-tag {
		color: rgba(255, 255, 255, 0.95);
	}

	/* Variante: Modelo base UNAL */
	.m-base .tick {
		width: 2px;
		height: 9px;
		background: oklch(0.78 0.18 304);
	}

	.m-base .m-val {
		color: oklch(0.88 0.16 304);
		font-size: 10.5px;
	}

	.m-base .m-tag {
		color: oklch(0.78 0.12 304);
		font-weight: 600;
	}

	/* Foco accesible */
	.marker:focus-visible .m-content {
		outline: 1.5px solid oklch(0.78 0.18 304);
		outline-offset: 3px;
		border-radius: 3px;
	}

	/* ── Tooltip de marcador ─────────────────────────────────────── */
	.m-tooltip {
		position: absolute;
		bottom: calc(100% + 6px);
		left: 50%;
		transform: translateX(-50%);
		width: 220px;
		max-width: 220px;
		padding: 0.65rem 0.8rem;
		background: #fff;
		border-left: 3px solid #1e3a5f;
		border-radius: 0.45rem;
		box-shadow: 0 6px 22px rgba(0, 0, 0, 0.28);
		font-size: 11px;
		line-height: 1.5;
		color: oklch(0.28 0.07 304);
		text-align: left;
		visibility: hidden;
		opacity: 0;
		transition:
			opacity 0.18s ease,
			visibility 0.18s ease;
		pointer-events: none;
		z-index: 30;
	}

	.marker:hover .m-tooltip,
	.marker:focus-within .m-tooltip {
		visibility: visible;
		opacity: 1;
		pointer-events: auto;
	}

	.marker.edge-left .m-tooltip {
		left: 0;
		transform: none;
	}

	.marker.edge-right .m-tooltip {
		left: auto;
		right: 0;
		transform: none;
	}

	.mt-body {
		display: block;
	}

	.m-base .m-tooltip {
		border-left-color: oklch(0.55 0.22 304);
	}

	.m-base .mt-body {
		color: oklch(0.5 0.04 304);
		font-style: italic;
	}

	.mt-link {
		display: inline-block;
		margin-top: 0.4rem;
		font-size: 10px;
		color: #1e3a5f;
		text-decoration: underline;
		font-weight: 600;
	}

	.mt-link:hover {
		color: #0f1f3a;
	}

	/* Métricas */
	.metrics {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 1rem;
		margin-bottom: 0.6rem;
	}

	@media (max-width: 680px) {
		.metrics {
			grid-template-columns: 1fr;
		}
	}

	.metric {
		border-radius: 0.75rem;
		padding: 1.2rem 1.4rem;
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
		transition: all 0.3s ease;
	}

	.mcost {
		background: oklch(0.35 0.08 350 / 0.2);
		border: 1px solid oklch(0.6 0.1 350 / 0.4);
	}

	.msav {
		background: oklch(0.55 0.22 304 / 0.18);
		border: 1px solid oklch(0.7 0.2 304 / 0.4);
	}

	.ml {
		font-size: 0.72rem;
		text-transform: uppercase;
		letter-spacing: 1px;
		opacity: 0.68;
	}

	.mv {
		font-family: 'Sekuya', serif;
		font-size: clamp(1.1rem, 2.5vw, 1.4rem);
		letter-spacing: 1.5px;
		transition: all 0.3s ease;
	}

	.mcost .mv {
		color: oklch(0.82 0.1 5);
	}

	.msav .mv {
		color: oklch(0.88 0.18 304);
	}

	.mbal {
		background: rgba(255, 255, 255, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.2);
	}

	.mbal.pos .mv {
		color: oklch(0.88 0.18 304);
	}

	.mbal.neg .mv {
		color: oklch(0.82 0.1 5);
	}

	/* ── Nota CAPEX ──────────────────────────────────────────────── */
	.capex-note {
		text-align: center;
		font-size: 0.76rem;
		color: rgba(255, 255, 255, 0.55);
		margin: 0 0 1.4rem 0;
		letter-spacing: 0.5px;
	}

	/* ── Botón colapsable ────────────────────────────────────────── */
	.expand-btn {
		width: 100%;
		padding: 0.78rem 1rem;
		background: transparent;
		color: #fff;
		border: 1px solid oklch(0.7 0.18 304);
		border-radius: 0.6rem;
		font-family: inherit;
		font-size: 0.88rem;
		font-weight: 600;
		letter-spacing: 0.6px;
		cursor: pointer;
		transition:
			background 0.2s,
			border-color 0.2s,
			transform 0.15s;
	}

	.expand-btn:hover {
		background: oklch(0.58 0.26 304 / 0.18);
		border-color: oklch(0.78 0.22 304);
	}

	.expand-btn:active {
		transform: translateY(1px);
	}

	/* ── Card de desglose ────────────────────────────────────────── */
	.breakdown {
		margin-top: 1.1rem;
		background: rgba(255, 255, 255, 0.97);
		color: oklch(0.28 0.07 304);
		border-radius: 1rem;
		padding: 1.6rem 1.4rem;
	}

	.sub {
		padding-left: 0.95rem;
		margin-bottom: 1.6rem;
	}

	.sub:last-of-type {
		margin-bottom: 0.4rem;
	}

	.sub-personal {
		border-left: 4px solid oklch(0.58 0.26 304);
	}

	.sub-fijos {
		border-left: 4px solid oklch(0.78 0.015 304);
	}

	.sub-title {
		font-size: 0.88rem;
		text-transform: uppercase;
		letter-spacing: 1.5px;
		color: oklch(0.32 0.18 304);
		margin: 0 0 0.85rem 0;
	}

	.sub-fijos .sub-title {
		color: oklch(0.45 0.04 304);
	}

	.row {
		padding: 0.9rem 0.95rem;
		border-radius: 0.55rem;
		background: oklch(0.98 0.012 304);
		margin-bottom: 0.6rem;
		border-left: 3px solid var(--accent, oklch(0.78 0.015 304));
	}

	.row-head {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 0.85rem;
		align-items: start;
	}

	@media (max-width: 580px) {
		.row-head {
			grid-template-columns: auto 1fr;
		}
		.row-amounts {
			grid-column: 1 / -1;
			align-items: flex-start !important;
			text-align: left !important;
			margin-top: 0.4rem;
		}
	}

	.row-icon {
		font-size: 1.3rem;
		line-height: 1.2;
	}

	.row-text {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
	}

	.row-text strong {
		font-size: 0.94rem;
		color: oklch(0.22 0.18 304);
		font-weight: 700;
	}

	.row-desc {
		font-size: 0.76rem;
		color: oklch(0.48 0.05 304);
		line-height: 1.45;
	}

	.row-amounts {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 0.15rem;
		text-align: right;
		white-space: nowrap;
	}

	.amount-annual {
		font-family: 'Sekuya', serif;
		font-size: 0.95rem;
		letter-spacing: 1px;
		color: var(--accent, oklch(0.35 0.22 304));
	}

	.row-fixed .amount-annual {
		color: oklch(0.32 0.18 304);
	}

	.amount-monthly {
		font-size: 0.74rem;
		color: oklch(0.5 0.05 304);
	}

	.src-link {
		display: inline-block;
		margin-top: 0.55rem;
		font-size: 0.72rem;
		color: oklch(0.42 0.22 304);
		text-decoration: none;
		border-bottom: 1px dashed oklch(0.42 0.22 304 / 0.45);
		transition:
			color 0.18s,
			border-color 0.18s;
	}

	.src-link:hover {
		color: oklch(0.32 0.22 304);
		border-bottom-color: oklch(0.32 0.22 304);
	}

	/* Badges */
	.badge {
		display: inline-block;
		margin-top: 0.35rem;
		padding: 0.18rem 0.6rem;
		border-radius: 9999px;
		font-size: 0.62rem;
		font-weight: 700;
		letter-spacing: 0.5px;
		text-transform: uppercase;
		width: max-content;
	}

	.badge-once {
		background: oklch(0.93 0.1 65);
		color: oklch(0.42 0.16 50);
	}

	.badge-recurring {
		background: oklch(0.93 0.07 240);
		color: oklch(0.42 0.18 250);
	}

	/* Tooltip */
	.tooltip-wrap {
		position: relative;
		display: inline-block;
		margin-left: 4px;
		white-space: normal;
	}

	.info-icon {
		display: inline-block;
		color: oklch(0.55 0 0);
		font-size: 12px;
		line-height: 1;
		cursor: pointer;
		user-select: none;
		vertical-align: middle;
	}

	.info-icon:focus {
		outline: 1.5px solid oklch(0.55 0.18 304);
		outline-offset: 2px;
		border-radius: 50%;
	}

	.tooltip-card {
		position: absolute;
		right: 0;
		top: calc(100% + 0.5rem);
		width: 240px;
		max-width: 240px;
		padding: 0.7rem 0.85rem;
		background: #fff;
		color: oklch(0.28 0.07 304);
		border-left: 3px solid oklch(0.32 0.18 304);
		border-radius: 0.5rem;
		box-shadow: 0 4px 18px rgba(0, 0, 0, 0.18);
		font-size: 11px;
		line-height: 1.55;
		text-align: left;
		visibility: hidden;
		opacity: 0;
		transition:
			opacity 0.18s ease,
			visibility 0.18s ease;
		z-index: 10;
		pointer-events: none;
	}

	.tooltip-wrap:hover .tooltip-card,
	.tooltip-wrap:focus-within .tooltip-card {
		visibility: visible;
		opacity: 1;
		pointer-events: auto;
	}

	.tt-title {
		display: block;
		font-size: 11px;
		color: oklch(0.22 0.18 304);
		margin-bottom: 0.35rem;
		font-weight: 700;
	}

	.tt-link {
		display: block;
		margin-top: 0.45rem;
		font-size: 10px;
		color: oklch(0.32 0.18 304);
		text-decoration: underline;
	}

	.tt-link:hover {
		color: oklch(0.22 0.18 304);
	}

	/* Footnote */
	.footnote {
		margin: 1rem 0 0 0;
		padding-top: 0.85rem;
		border-top: 1px solid oklch(0.93 0.02 304);
		font-size: 0.72rem;
		line-height: 1.7;
		color: oklch(0.5 0.05 304);
		text-align: center;
	}

	.footnote a {
		font-size: 10px;
		color: oklch(0.32 0.18 304);
		text-decoration: underline;
	}

	.footnote a:hover {
		color: oklch(0.22 0.18 304);
	}

	/* ── POR QUÉ FUNCIONA ────────────────────────────────────────── */
	.why {
		background: oklch(0.97 0.025 304);
	}

	.why .wrap {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 2.5rem;
	}

	.why-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1.5rem;
		width: 100%;
	}

	.why-card {
		background: #fff;
		border-radius: 1rem;
		padding: 2rem 1.75rem;
		border-top: 4px solid oklch(0.58 0.26 304);
		box-shadow: 0 2px 16px oklch(0.5 0.15 304 / 0.1);
	}

	.why-card h3 {
		font-size: 0.88rem;
		color: oklch(0.35 0.22 304);
		margin: 0 0 1rem 0;
		text-transform: uppercase;
	}

	.why-card p {
		font-size: 0.9rem;
		line-height: 1.72;
		color: oklch(0.28 0.07 304);
		margin: 0;
	}

	/* ── FOOTER ──────────────────────────────────────────────────── */
	footer {
		background: oklch(0.17 0.15 307);
		color: rgba(255, 255, 255, 0.45);
		text-align: center;
		padding: 2rem 1rem;
		font-size: 0.78rem;
		letter-spacing: 0.5px;
		line-height: 1.6;
	}

	footer p {
		margin: 0;
	}
</style>
