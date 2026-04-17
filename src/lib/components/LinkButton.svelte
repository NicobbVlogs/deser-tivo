<script lang="ts">
    import type { Snippet } from "svelte";
    const { href, children }: { href: string; children: Snippet<[]> } =
        $props();
</script>

<a {href}>
    {@render children()}
</a>

<style>
    a {
        text-decoration: none;
        text-align: center;

        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;

        padding: 1rem;
        max-width: 10em;

        border: 3px solid light-dark(oklch(0.4 0.1 304), oklch(0.5 0.1 304));
        background: light-dark(oklch(0.8 0.1 304), oklch(0.4 0.1 304));
        color: light-dark(oklch(0.3 0.1 304), oklch(0.9 0.1 304));
    }
</style>
