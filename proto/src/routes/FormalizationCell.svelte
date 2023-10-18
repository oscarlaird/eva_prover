<script>
    import Editor from "./Editor.svelte";
    import leanLexer from "$lib/lexers/lean.js";
    export let nl_math = "";
    export let lean_statement = "";
    export let proof_trace = [];
    let layers = ["",""];
    $: syntax_layers = leanLexer(lean_statement);
    $: layers[0] = syntax_layers[0];
    $: layers[1] = syntax_layers[1];
    $: editor_height = (lean_statement.split("\n").length + 1) + "em";

    function autoformalize() {
        lean_statement = "autoformalizing...";
        fetch("http://localhost:8000/autoformalize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ nl_problem: nl_math }),
        })
        .then(response => response.json())
        .then(data => {
            lean_statement = data.lean_statement;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }

    // reset the proof_trace when the lean_statement changes
    function reset_proof_trace() {
        fetch("http://localhost:8000/init_search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(lean_statement),
        })
        .then(response => response.json())
        .then(data => {
            proof_trace = [data];
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }

    $: if (lean_statement != "") {
        reset_proof_trace();
    }
</script>

<div class="container">
    <Editor bind:code={lean_statement}
            bind:layers
            editor_height={editor_height} />
    <div class="autoformalize_button">
        <button on:click={autoformalize}>Autoformalize</button>
    </div>
</div>

<style>
    .container {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .autoformalize_button {
        position: absolute;
        top: 4px;
        right: 0;
    }
</style>