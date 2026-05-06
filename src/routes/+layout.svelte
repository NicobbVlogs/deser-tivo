<script lang="ts">
	import "@fontsource/sekuya";
	import "@fontsource-variable/ibm-plex-sans";

	import "../default.css";
	import favicon from "$lib/assets/favicon.svg";

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<h1>Deser-tiva</h1>

<nav>
	<a href="predecir" class="part-btn">
		<span class="part-num">Primera Parte</span>
		<span class="part-name">LA DESERCIÓN</span>
	</a>
	<a href="estimar-eficiencia" class="part-btn">
		<span class="part-num">Segunda Parte</span>
		<span class="part-name">LA INVERSIÓN</span>
	</a>
</nav>

{@render children()}

<style>
	h1 {
		text-align: center;
		font-size: min(15vw, 5rem);
		text-transform: uppercase;
	}

	nav {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 1.25rem;
		margin-bottom: 4rem;
	}

	.part-btn {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 0.25rem;
		text-decoration: none;
		padding: 1.4rem 2.8rem;
		min-width: 210px;
		border-radius: 14px;
		background: linear-gradient(
			140deg,
			light-dark(oklch(0.38 0.2 304), oklch(0.32 0.2 304)),
			light-dark(oklch(0.28 0.18 310), oklch(0.22 0.18 310))
		);
		color: #fff;
		border: 1px solid light-dark(oklch(0.5 0.2 304 / 0.4), oklch(0.6 0.2 304 / 0.3));
		box-shadow:
			0 4px 20px light-dark(oklch(0.38 0.2 304 / 0.35), oklch(0.3 0.2 304 / 0.5)),
			inset 0 1px 0 rgba(255, 255, 255, 0.1);
		transition:
			transform 0.15s ease,
			box-shadow 0.15s ease;
	}

	.part-btn:hover {
		transform: translateY(-3px);
		box-shadow:
			0 8px 28px light-dark(oklch(0.38 0.2 304 / 0.5), oklch(0.3 0.2 304 / 0.65)),
			inset 0 1px 0 rgba(255, 255, 255, 0.15);
	}

	.part-num {
		font-size: 0.7rem;
		letter-spacing: 2.5px;
		text-transform: uppercase;
		opacity: 0.65;
	}

	.part-name {
		font-family: "Sekuya", serif;
		font-size: 1.15rem;
		letter-spacing: 3px;
	}
</style>
