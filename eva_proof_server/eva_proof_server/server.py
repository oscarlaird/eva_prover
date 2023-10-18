from fastapi import FastAPI
from fastapi import HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

import eva_proof_server.lean_repl as lean_repl
import eva_proof_server.interface as interface
import eva_proof_server.suggest_math as suggest_math
import eva_proof_server.autoformalize as autoformalize

from eva_proof_server.autoprove import router as autoprove_router

app = FastAPI()
app.include_router(autoprove_router)

origins = [
    "http://localhost",
    "http://localhost:8080",  # Adjust as per your frontend server
    "http://localhost:5173",  # Adjust as per your frontend server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# suggestion
@app.post("/suggest", response_model=interface.SuggestionOutput)
async def suggest(input: interface.SuggestionInput = Body(...)):
    return interface.SuggestionOutput(suggestion=" world")
    suggestion = cursor.query(f"""
        SELECT OpenAIChatCompletion(
            'Complete the text. Do not repeat the users text. Return only the completion
                              with no explanation. You are provided with what the user has typed.',
            '{input.word}'
        )
    """).df().iloc[0]['openaichatcompletion.response']
    return SuggestionOutput(suggestion=suggestion)

# autoformalize
@app.post("/autoformalize", response_description=interface.autoformalize_description, response_model=interface.AutoformalizeOutput)
async def _autoformalize(input: interface.AutoformalizeInput = Body(...)):
    return interface.AutoformalizeOutput(lean_statement=autoformalize.autoformalize(input.nl_problem))