// Perform syntax highlighting on LaTeX code.
// A simple lexer that reads through the file one character at a time.
// Returns a list of layers where characters that don't belong to a layer are replaced with spaces.

export default function latexLexer(text) {
    // we have three layers: text, math, and command
    let layers = Array(3).fill("");
    let math = false; // whether we are in math mode
    let command = false; // whether we are in a command
    // TODO invalid commands, double math mode, markdown
    // iterate thru the text one character at a time
    let selected_layer = 0;
    let c;
    for (let i = 0; i < text.length; i++) {
        c = text[i];
        // check for commands
        if (c === "\\") {
            command = true;
            selected_layer = 2;
        } else if (command) {
            selected_layer = 2;
            if (c === " " || c === "\n" || c === "\\") {
                command = false;
            }
        } else if (c === "$") {
            math = !math;
            selected_layer = 1;
        } else if (math) {
            selected_layer = 1;
        }
        // otherwise, we are in text mode
        else {
            selected_layer = 0;
        }
        // add the character to the selected layer, add a space to the other layers.
        for (let j = 0; j < layers.length; j++) {
            layers[j] += j === selected_layer ? c : " ";
        }
    }
    return layers;
}

