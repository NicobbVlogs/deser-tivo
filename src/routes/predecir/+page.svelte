<script lang="ts">
    import Riesgo from "$lib/components/Riesgo.svelte";
    import { fade } from "svelte/transition";

    let socioeconómica = $state(25);
    let papa = $state(3.0);
    let avance = $state(40);
    let apoyoAlimentario = $state("1");
    let admisiónEspecial = $state("0");
    let sanciónAcadémica = $state("1");
</script>

<div transition:fade={{ duration: 150 }} id="container">
    <p>
        Introduzca las variables independientes que desee y vea cómo afectan la
        estimación de riesgo del modelo.
    </p>

    <h2>Características del estudiante</h2>
    <form>
        <div class="question">
            <label for="selección-socioeconómica">PBM socioeconómico</label>
            <input
                type="number"
                id="selección-socioeconómica"
                name="socioeconómica"
                min="0"
                max="100"
                bind:value={socioeconómica}
            />
        </div>

        <div class="question">
            <label for="selección-papa">PAPA acumulado</label>
            <input
                type="number"
                id="selección-papa"
                name="papa"
                min="0"
                max="5"
                step="0.1"
                bind:value={papa}
            />
        </div>

        <div class="question">
            <label for="selección-avance"
                >Avance en la carrera, como porcentaje</label
            >
            <input
                type="number"
                id="selección-avance"
                name="avance"
                min="0"
                max="100"
                bind:value={avance}
            />
        </div>

        <div class="question">
            <label for="selección-apoyo-alimentario"
                >¿Recibe apoyo alimentario?</label
            >
            <select
                id="selección-apoyo-alimentario"
                name="apoyo-alimentario"
                bind:value={apoyoAlimentario}
            >
                <option value="0">No</option>
                <option value="1">Sí</option>
            </select>
        </div>

        <div class="question">
            <label for="selección-admisión-especial"
                >¿Recibió admisión especial?</label
            >
            <select
                id="selección-admisión-especial"
                name="admisión-especial"
                bind:value={admisiónEspecial}
            >
                <option value="0">No</option>
                <option value="1">Sí</option>
            </select>
        </div>

        <div class="question">
            <label for="selección-sanción-académica"
                >¿Recibió una sanción académica?</label
            >
            <select
                id="selección-sanción-académica"
                name="sanción-académica"
                bind:value={sanciónAcadémica}
            >
                <option value="0">No</option>
                <option value="1">Sí</option>
            </select>
        </div>
    </form>

    <h2>Resultados</h2>

    {#await import("$lib/modelo") then m}
        <Riesgo
            given={m.default([
                socioeconómica,
                papa,
                avance,
                Number(apoyoAlimentario),
                Number(admisiónEspecial),
                Number(sanciónAcadémica),
            ])}
        ></Riesgo>
    {/await}
</div>

<style>
    label,
    select,
    input {
        display: flex;
    }

    select,
    input {
        appearance: base-select;
        min-width: 3.5rem;
    }

    label {
        margin-bottom: 0.5rem;
    }

    #container {
        max-width: 500px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;

        p {
            margin: 0.2rem;
        }
    }

    form {
        width: 90%;
    }

    .question {
        display: flex;
        flex-direction: row;
        gap: 2rem;
        justify-content: space-between;
        width: 100%;
        margin: 0.4rem 0;
    }
</style>
