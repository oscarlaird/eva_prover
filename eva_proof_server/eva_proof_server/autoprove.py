from fastapi import APIRouter, Body, Depends
import eva_proof_server.interface as interface
import eva_proof_server.lean_repl as lean_repl
import eva_proof_server.reprover as reprover

router = APIRouter()

REPL = lean_repl.open_repl()
async def get_repl_process():
    """Open a Lean REPL subprocess."""
    return REPL

ROOT_STATE = interface.ProofState(tactic_state="", proof_steps=[], error=None, search_id="0", tactic_state_id="0")

# init_search
@router.post("/init_search", response_model=interface.ProofState)
async def init_search(conjecture: str = Body(...), REPL=Depends(get_repl_process)):
    # Create the initial search state
    conjecture_command = ["conjecture_set", ["0", "0", conjecture]]
    return lean_repl.send_command_to_repl(conjecture_command, REPL)

# run_tac 
@router.post("/run_tac", response_model=interface.ProofState)
async def run_tac(input: interface.ProofState = Body(...), REPL=Depends(get_repl_process)):
    # the tactic is passed in the proof_steps field
    tactic = input.proof_steps[-1]
    command = ["run_tac", [input.search_id, input.tactic_state_id, tactic]]
    new_state = lean_repl.send_command_to_repl(command, REPL)
    new_state.proof_steps = input.proof_steps
    return new_state

# auto step (return the first suggested tactic that works)
@router.post("/autostep", response_model=interface.ProofState)
async def auto_step(input: interface.ProofState = Body(...), REPL=Depends(get_repl_process)):
    possible_tactics = ["intros"] + reprover.suggest_tactics(goal = input.tactic_state)
    for tactic in possible_tactics:
        command = ["run_tac", [input.search_id, input.tactic_state_id, tactic]]
        new_state = lean_repl.send_command_to_repl(command, REPL)
        new_state.proof_steps = input.proof_steps + [tactic]
        if not new_state.error and new_state.tactic_state != input.tactic_state:
            return new_state