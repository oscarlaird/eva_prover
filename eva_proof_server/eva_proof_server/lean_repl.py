from fastapi import APIRouter, HTTPException, Body
from eva_proof_server.interface import ProofState

import subprocess
import json
import os
from pathlib import Path


def send_command_to_repl(command, subprocess_obj):
    """Send a JSON-encoded message to the Lean REPL."""
    json_str = json.dumps(command) + '\n'  # Add newline to signal end of message
    subprocess_obj.stdin.write(json_str)
    subprocess_obj.stdin.flush()
    line = subprocess_obj.stdout.readline()
    print('_-------------------')
    print(line)
    return ProofState(**json.loads(line))

def open_repl():
    """Open a Lean REPL subprocess."""
    os.chdir("/home/oscar/nlitp/lean-gym")
    repl_process = subprocess.Popen(
        ["lean", "--run", "src/repl.lean"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,  # Line-buffered
        text=True,  # Read and write strings
    )
    init_command = ["init_search", ["mathd_algebra_35", ""]]
    response = send_command_to_repl(init_command, repl_process)
    assert response.error is None
    assert response.search_id == response.tactic_state_id == '0'
    return repl_process

def run_proof_steps(target, proof_steps, subprocess_obj):
    """Initialize a search in the Lean REPL, set a target, and run proof steps."""
    # Initialize the search and set the target
    conjecture_command = ["conjecture_set", ["0", "0", target]]

    state = send_command_to_repl(conjecture_command, subprocess_obj)

    # Run proof steps
    for step in proof_steps:
        step_command = ["run_tac", [state.search_id, state.tactic_state_id, step]]
        state = send_command_to_repl(step_command, subprocess_obj)
        # Break early if an error occurs
        if state.error:
            break
    
    return state

# run the repl script at /home/oscar/nlitp/lean-gym/src/lean.repl
# initialize the search with
#  ["init_search", ["int.prime.dvd_mul", ""]]
# set the target with
#  ["conjecture_set", ["0","0",{target}]]
# go thru the proof steps with
#  ["run_tac", ["0","0",{proofsteps[i]}]]
# every time the lean repl will reply with a message like
# {"error":null,"proof_steps":[],"search_id":"0","tactic_state":"m n : ℤ,\np : ℕ,\nhp : nat.prime p,\nh : ↑p ∣ m * n\n⊢ p ∣ m.nat_abs * n.nat_abs","tactic_state_id":"2"}
# return the error message and the goals (aka tactic_state) to the frontend
# stop early if any of the proof steps raise an error