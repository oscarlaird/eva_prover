<script>
  import { onMount } from "svelte";
  import MarkdownIt from "markdown-it";
  import mk from "markdown-it-katex";
  import Editor from "./Editor.svelte";
  import latexLexer from "$lib/lexers/latex.js";
  
  // Editor props
  export let input = "";
  let layers = ["","","",""];
  $: editor_height = ((input + suggestion_remainder).split("\n").length + 10) + "em";

  // syntax highlighting
  $: syntax_layers = latexLexer(input);
  $: layers[1] = syntax_layers[0];
  $: layers[2] = syntax_layers[1];
  $: layers[3] = syntax_layers[2];

  // autocomplete
  let suggestion = "";
  $: full_suggestion = suggestion_prompt + suggestion
  $: suggestion_remainder = full_suggestion.slice(0,input.length) === input ? 
    full_suggestion.slice(input.length, full_suggestion.length) :
    "";
  $: layers[0] = input.replace(/./g," ") + suggestion_remainder;
  // the suggestion is fetched from the server
  let timeout;
  let suggestion_prompt = "";
  let new_suggestion_prompt = "";
  $: if (input) {
    // Clear the timeout if it has already been set.
    clearTimeout(timeout);

    // Call suggest endpoint after 500ms
    timeout = setTimeout(() => {
      new_suggestion_prompt = input;
      fetch("http://localhost:8000/suggest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ word: input }),
      })
      .then(response => response.json())
      .then(data => {
        suggestion_prompt = new_suggestion_prompt;
        suggestion = data.suggestion;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    }, 500);
  }

  // event handlers
  let editing = false;
  function handleInput(event) {
    if (event.key === "Enter" && (event.ctrlKey || event.shiftKey)) {
      event.preventDefault();
      editing = false;
    } else if (event.key === "Tab") {
      event.preventDefault();
      input += suggestion;
    }
  }

  // Render the markdown
  let md = new MarkdownIt();
  md.use(mk);
  $: output = md.render(input) || "<i>Click to type Math...</i>";
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-positive-tabindex -->
<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
<div class="container"
    on:click={() => (editing = true)}
    tabindex="0"
    >
{#if editing}
  <Editor bind:code={input} editor_height={editor_height}
          handle_keydown={handleInput} handle_blur={() => (editing = false)}
          bind:layers />
{/if}
<div class="output" >
{@html output}
</div>
</div>

<style>
  .container {
    cursor: pointer;
  }
</style>
