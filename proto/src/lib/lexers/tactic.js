// Perform syntax highlighting on Lean tactics.
// A tactic has the following syntax:
// tactic [premise1, premise2]
// Returns a list of layers where characters that don't belong to a layer are replaced with spaces.

export default function tacticLexer(text) {
    // we have three layers: tactic, bracket, premise
    let layers = Array(3).fill("");
    // iterate thru the text one character at a time
    let premise_list = false;
    let selected_layer = 0;
    let c;
    for (let i = 0; i < text.length; i++) {
        c = text[i];
        // check for commands
        if (c === "[") {
            premise_list = true;
            selected_layer = 1;
        } else if (c === "]") {
            premise_list = false;
            selected_layer = 1;
        } else if (c === ",") {
            selected_layer = 1;
        } else if (premise_list) {
            selected_layer = 2;
        } else {
            selected_layer = 0;
        }
        // add the character to the selected layer, add a space to the other layers.
        for (let j = 0; j < layers.length; j++) {
            layers[j] += j === selected_layer ? c : " ";
        }
    }
    return layers;
}