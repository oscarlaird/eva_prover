<script>
    import MathCell from './MathCell.svelte';
    import FormalizationCell from './FormalizationCell.svelte';
    import ProofSteps from './ProofSteps.svelte';
    import TacticEditor from './TacticEditor.svelte';
    import Node from './Node.svelte';

    let empty_child_template = {
        nl_math: 'For all integers $n \\geq 9$ , the value of $\\frac{(n + 2)! - (n + 1)!}{n!}$ is a perfect square.',
        lean_statement: '',
        proof_trace: [],
        children: []
    }
    // the node must be a deep copy of the empty_child_template. A shallow copy would make `children` a reference to the same array
    let make_empty_child = () => JSON.parse(JSON.stringify(empty_child_template));
    export let node = make_empty_child();
    // callback for add_child button
    function add_child() {
        node.children.push(make_empty_child()); // push a new empty child to the children array
        node = node; // this doesn't automatically trigger an update, so we need to force it
    }

</script>

<!--
    NODE
    - nl_math: the natural language math statement   (also button to kill node)
    - lean_statement: the lean statement             (button to autoformalize from nl_math)
    - goal: the goal of the proofstep (only show if open)
    - next_tactic editor (only show if open) (include tactic suggestions)
    - CHILD NODES
    - add child button
-->

<div class="container">
    <div class="node">
    <MathCell bind:input={node.nl_math} />
    <FormalizationCell bind:lean_statement={node.lean_statement} nl_math={node.nl_math}
                       bind:proof_trace={node.proof_trace} />
    {#if node.proof_trace}
        <ProofSteps bind:proof_trace={node.proof_trace} />
    {/if}
    <!-- add child -->
    <button on:click={add_child}>Add Child</button>
    </div>
    {#each node.children as child}
            <Node bind:node={child} />
    {/each}
</div>

<style>
    .node {
        border: 1px solid black;
    }
    .container {
        margin-left: 3em;
    }
</style>