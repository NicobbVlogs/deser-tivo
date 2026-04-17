<script lang="ts">
	import "@fontsource/sekuya";
	import "@fontsource-variable/ibm-plex-sans";

	import LinkButton from "$lib/components/LinkButton.svelte";
	import "../default.css";
	import favicon from "$lib/assets/favicon.svg";

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<h1>Deser-tiva</h1>

<ul>
	<li>
		<LinkButton href="predecir">Consultar riesgo de deserción</LinkButton>
	</li>
	<li>
		<LinkButton href="estimar-eficiencia"
			>Definir parámetros para cálculo de comparativa</LinkButton
		>
	</li>
</ul>

{@render children()}

<style>
	h1 {
		text-align: center;
		font-size: min(15vw, 5rem);
		text-transform: uppercase;
	}

	ul {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 1rem;

		margin-bottom: 5rem;

		list-style-type: none;
		padding: 0;
	}
</style>
