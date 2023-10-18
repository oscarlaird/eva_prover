<script>
    import Editor from "./Editor.svelte";
    import tacticLexer from "$lib/lexers/tactic.js";
    export let proof_trace;
    let new_tactic = "";
    let layers = ["","","",""];
    $: syntax_layers = tacticLexer(new_tactic);
    $: layers[0] = syntax_layers[0];
    $: layers[1] = syntax_layers[1];
    $: layers[2] = syntax_layers[2];
    function handleKeydown(event) {
        // Press enter to submit tactic.
        if (event.key === "Enter") {
            event.preventDefault();
            let send_state = JSON.parse(JSON.stringify(proof_trace[proof_trace.length - 1]));
            send_state.proof_steps = [new_tactic];
            fetch("http://localhost:8000/run_tac", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(send_state),
            })
            .then(response => response.json())
            .then(data => {
                proof_trace = [...proof_trace, data];
                new_tactic = "";
            })
        }
    }
    function autostep (again=false) {
        let send_state = JSON.parse(JSON.stringify(proof_trace[proof_trace.length - 1]));
        fetch("http://localhost:8000/autostep", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(send_state),
        })
        .then(response => response.json())
        .then(data => {
            proof_trace = [...proof_trace, data];
            new_tactic = "";
            if (again) {
                autostep(true);
            }
        })
    }
</script>

<div class="container">
    <Editor bind:code={new_tactic} bind:layers handle_keydown={handleKeydown} />
    <div class="autoprove_button">
        <button on:click={() => autostep(false)}>Autostep</button>
        <button on:click={() => autostep(true)}>Autoprove</button>
    </div>
</div>


<style>
    .container {
        position: relative;
    }
    .autoprove_button {
        position: absolute;
        right: 0;
        top: 4px;
    }
</style>