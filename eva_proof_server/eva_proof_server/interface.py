from pydantic import BaseModel

class SuggestionInput(BaseModel):
    word: str
class SuggestionOutput(BaseModel):
    suggestion: str = None

class AutoformalizeInput(BaseModel):
    nl_problem: str
class AutoformalizeOutput(BaseModel):
    lean_statement: str = None
autoformalize_description = "The formal statement generated by GPT-3 from the given natural language problem."

class ProofState(BaseModel):
    tactic_state: str = None
    proof_steps: list[str]
    error: str = None
    search_id: str = None
    tactic_state_id: str = None

class ProofTrace(BaseModel):
    states: list[ProofState]