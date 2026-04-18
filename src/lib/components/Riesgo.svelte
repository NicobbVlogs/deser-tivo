<script lang="ts">
    const { given } = $props();
    const [_, dropout] = $derived(given);
</script>

<p>
    La probabilidad de deserción se estima en <strong
        >{Math.round(dropout * 100)}%</strong
    >.
</p>

{#if dropout > 0.8}
    <p class="high">El riesgo es alto.</p>
{:else if dropout > 0.5}
    <p class="moderate">El riesgo es moderado.</p>
{:else}
    <p class="low">El riesgo es bajo.</p>
{/if}
