<script>
    export let proof_trace;
    import TacticEditor from "./TacticEditor.svelte";
    $: goal = (proof_trace.length > 0 && !proof_trace[0].error) ? proof_trace[proof_trace.length - 1].tactic_state : "Not formalized.";
    let display_goal = null;
    $: if (proof_trace) {
        display_goal = null; // clear the display goal when the proof trace changes
    }
    // $: display_goal_bg = display_goal === "no goals" ? "green" : (proof_trace.length > 0 ? "yellow" : "red");
    $: display_goal_bg = display_goal != null ? "yellow" : (goal === "no goals" ? "green" : goal === "Not formalized." ? "red" : "yellow");
</script>

<div class="proofsteps">
    {#each proof_trace as state, i}
        {#if i > 0}
        <div class="step"
            on:click={() => {proof_trace = proof_trace.slice(0, i); }}
            on:mouseenter={() => display_goal = proof_trace[i - 1].tactic_state}
            on:mouseleave={() => display_goal = null}
            >
            {state.proof_steps[state.proof_steps.length - 1]}
        </div>
        {/if}
    {/each}
</div>

<pre style:background-color={display_goal_bg}>
{display_goal != null ? display_goal : goal}
</pre>
{#if goal != "Not formalized." && goal != "no goals"}
    <TacticEditor bind:proof_trace={proof_trace} />
{/if}

<style>
    .proofsteps {
        display: flex;
        flex-direction: column;
        align-items: left;
    }
    /* hover over a step to see the goal */
    .step:hover {
        background-color: #d4da83;
    }
    pre {
        font-family: monospace;
        font-size: 1.2em;
        background-color: antiquewhite;
    }
</style>