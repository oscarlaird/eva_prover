// Perform syntax highlighting on Lean formalizations.
// divide it into two parts: hypothesis and goal
// A statement has the following syntax:
// (hyp) (hyp) : goal
// Returns a list of two layers where characters that don't belong to a layer are replaced with spaces.

export default function tacticLexer(text) {
    // we have two layers: hypothesis and goal
    let layers = Array(2).fill("");
    // iterate thru the text one character at a time
    let hypothesis = false; // whether we are in hypothesis
    let paren_count = 0; // number of parentheses
    let goal = false; // whether we are in goal
    let premise_list = false;
    let selected_layer = 0;
    let c;
    for (let i = 0; i < text.length; i++) {
        if (text[i] === "(") {
            paren_count++;
        } else if (text[i] === ")") {
            paren_count--;
        } else if (text[i] === ":" && paren_count === 0) {
            hypothesis = false;
            goal = true;
            selected_layer = 1;
        }
        // add the character to the selected layer, add a space to the other layers.
        for (let j = 0; j < layers.length; j++) {
            layers[j] += j === selected_layer ? text[i] : " ";
        }
    }
    return layers;
}