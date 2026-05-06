<script lang="ts">
	import { fade } from 'svelte/transition';

	let riskPool = $state(58);
	let mlPrecision = $state(80);
	let acceptanceRate = $state(60);
	let successRate = $state(47);

	const BASE = 6240;

	let step1 = $derived(Math.round(BASE * (riskPool / 100) * (mlPrecision / 100)));
	let step2 = $derived(Math.round(step1 * (acceptanceRate / 100)));
	let step3 = $derived(Math.round(step2 * (successRate / 100) * 0.68));
	let savingsM = $derived(parseFloat((step3 * 19.5).toFixed(1)));
	let costM = $derived(parseFloat((100 + step2 * 0.68 * 0.295).toFixed(1)));
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
					<div class="srow">
						<div class="slbl">
							<span>Tasa de identificación ML</span>
							<span class="sv">{riskPool}%</span>
						</div>
						<input type="range" min="10" max="90" step="5" bind:value={riskPool} />
					</div>
					<div class="srow">
						<div class="slbl">
							<span>Precisión del modelo ML</span>
							<span class="sv">{mlPrecision}%</span>
						</div>
						<input type="range" min="50" max="95" step="5" bind:value={mlPrecision} />
					</div>
					<div class="srow">
						<div class="slbl">
							<span>Tasa de aceptación del apoyo</span>
							<span class="sv">{acceptanceRate}%</span>
						</div>
						<input type="range" min="20" max="80" step="5" bind:value={acceptanceRate} />
					</div>
					<div class="srow">
						<div class="slbl">
							<span>Tasa de éxito de la intervención</span>
							<span class="sv">{successRate}%</span>
						</div>
						<input type="range" min="20" max="70" step="5" bind:value={successRate} />
					</div>
				</div>
			</div>

			<!-- Métricas financieras -->
			<div class="metrics">
				<div class="metric mcost">
					<span class="ml">Costo del sistema (anual)</span>
					<span class="mv">{fmt(costM)} M COP</span>
				</div>
				<div class="metric msav">
					<span class="ml">Pérdidas prevenidas (anual)</span>
					<span class="mv">{fmt(savingsM)} M COP</span>
				</div>
			</div>
			<p class="balance" class:pos={balanceM >= 0} class:neg={balanceM < 0}>
				Balance neto: {fmt(balanceM)} millones COP/año
			</p>
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
		gap: 1.6rem;
		padding: 1.75rem;
		background: rgba(255, 255, 255, 0.07);
		border-radius: 1rem;
		border: 1px solid rgba(255, 255, 255, 0.12);
	}

	.srow {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
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

	input[type='range'] {
		width: 100%;
		accent-color: oklch(0.68 0.26 304);
		cursor: pointer;
		height: 5px;
	}

	/* Métricas */
	.metrics {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1rem;
		margin-bottom: 1.25rem;
	}

	@media (max-width: 480px) {
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

	.balance {
		font-family: 'Sekuya', serif;
		font-size: clamp(1.1rem, 2.8vw, 1.65rem);
		letter-spacing: 2px;
		text-align: center;
		padding: 1rem 1.5rem;
		border-radius: 0.75rem;
		background: rgba(255, 255, 255, 0.07);
		margin: 0;
		transition: color 0.3s ease;
	}

	.balance.pos {
		color: oklch(0.88 0.18 304);
	}

	.balance.neg {
		color: oklch(0.82 0.1 5);
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
