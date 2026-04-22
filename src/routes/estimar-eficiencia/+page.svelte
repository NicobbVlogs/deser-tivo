<script>
    import trabajo1 from "$lib/assets/RESULTADOS/EN TRABAJO 1.jpeg";
    import trabajo2 from "$lib/assets/RESULTADOS/EN TRABAJO 2.jpeg";
    import { fade } from "svelte/transition";
</script>

<div transition:fade={{ duration: 150 }}>
    <img alt="Perrito trabajando" src={trabajo1} />
    <img alt="Miquito trabajando" src={trabajo2} />
</div>

<style>
    div {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
    }

    img {
        display: block;
        border-radius: 1rem;
        max-width: 300px;
    }
</style>
