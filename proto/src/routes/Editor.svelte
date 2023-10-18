<script>
    // TODO:
    // - vim keybindings are not necessary, the user can use an extension
    // - LSPs aren't needed for completion, copilot is the only autocompleter that matters
    // A simple code editor with syntax highlighting
    // Implemented with overlayed textareas
    export let code = '';
    export let layers = [];
    export let colors = ['green', 'blue', 'brown', 'gray', 'black'];
    export let handle_keydown = () => {};
    export let handle_blur = () => {};
    export let editor_height;
    export let placeholder;
</script>

<div class="container" style:height={editor_height}>
    <textarea bind:value={code} class="editor" on:keydown={handle_keydown} placeholder={placeholder} on:blur={handle_blur} autofocus></textarea>
    <!-- layers -->
    {#each layers as l, i}
        <textarea value={l} class="editor layer"
        style="z-index: {i}"
        style:color={colors[i]}
        readonly
        ></textarea>
    {/each}
</div>


<style>
    .container {
        position: relative;
        width: 100%;
        min-height: 2em;
    }
    /* position the textareas on top of each other */
    .editor {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        /* code mono font */
        font-size: 16px;
        font-family: monospace;
        /* make the textareas transparent */
        background: transparent;
        /* don't wrap lines */
        white-space: pre;
        overflow-x: auto;
    }
    .layer {
        /* make the textareas not editable */
        pointer-events: none;
    }
</style>