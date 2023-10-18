from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("kaiyuy/leandojo-lean3-tacgen-byt5-small")       # Or "lean3" -> "lean4"
model = AutoModelForSeq2SeqLM.from_pretrained("kaiyuy/leandojo-lean3-tacgen-byt5-small")   # Or "lean3" -> "lean4"

def suggest_tactics(goal):
    # state = "n : ℕ\n⊢ gcd n n = n"
    # state = "∀ (n : ℕ), 0 < n → nat.gcd n n = n"
    tokenized_goal = tokenizer(goal, return_tensors="pt")

    # Generate a single tactic.
    # tactic_ids = model.generate(tokenized_goal.input_ids, max_length=1024)
    # tactic = tokenizer.decode(tactic_ids[0], skip_special_tokens=True)
    # print(tactic, end="\n\n")

    # Generate multiple tactics via beam search.
    tactic_candidates_ids = model.generate(
        tokenized_goal.input_ids,
        max_length=1024,
        num_beams=40,
        length_penalty=0.0,
        do_sample=False,
        num_return_sequences=20,
        early_stopping=False,
    )
    tactic_candidates = tokenizer.batch_decode(
        tactic_candidates_ids, skip_special_tokens=True
    )

    # strip the <a> and </a> tags
    tactic_candidates = [t.replace("<a>", "").replace("</a>", "") for t in tactic_candidates]

    return tactic_candidates

if __name__=='__main__':
    print(suggest_tactics("n : ℕ\n⊢ gcd n n = n"))