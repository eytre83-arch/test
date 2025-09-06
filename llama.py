import json
import subprocess
import time

def ollama_generate(prompt: str) -> str:
    """Call LLaMA-3 model via Ollama CLI"""
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8")

def make_clones_with_llama(task: dict, n_clones=5, max_retries=3):
    """Generate strict math question clones with full multilingual support and structured output"""
    prompt = f"""
You are a professional assistant for generating mathematics questions for educational datasets.

Below is a sample question:
{json.dumps(task, ensure_ascii=False, indent=2)}

Your task is to generate exactly {n_clones} unique clones based on this sample. You must strictly follow the rules below:

🚫 Do NOT reuse the original question or its options in any clone.

✅ For each input question, generate exactly {n_clones} clones. Each clone must be unique and follow this exact JSON structure:

{{
  "id": "math-<number>-corrected",
  "number": <number>,
  "subject": "matematika",
  "topic": "<topic>",  // Must match the question content
  "tags": ["<tag1>", "<tag2>", "<tag3>"],
  "question": {{
    "uz": "<Uzbek question>",  // Fully translated, including numbers and formulas
    "ru": "<Russian question>",  // Fully translated, including numbers and formulas
    "en": "<English question>"  // Fully translated, including numbers and formulas
  }},
  "options": {{
    "A": {{ "uz": "$<A>$", "ru": "$<A>$", "en": "$<A>$" }},
    "B": {{ "uz": "$<B>$", "ru": "$<B>$", "en": "$<B>$" }},
    "C": {{ "uz": "$<C>$", "ru": "$<C>$", "en": "$<C>$" }},
    "D": {{ "uz": "$<D>$", "ru": "$<D>$", "en": "$<D>$" }}
  }},
  "answer": "<A|B|C|D>",  // Must match one of the options
  "difficulty": "<easy|medium|hard>",
  "language": ["uz", "ru", "en"],
  "solutions": [
    {{
      "method": "enumeration",
      "steps": ["<step1>", "<step2>"],  // Clear, logical steps
      "final_answer": "<numeric_string>"  // Must match one of the options
    }},
    {{
      "method": "formula",
      "steps": ["<step1>", "<step2>"],  // Clear, logical steps
      "final_answer": "<numeric_string>"  // Must match one of the options
    }}
  ],
  "explanation": {{
    "uz": "<explanation>",  // Clear and relevant to the question
    "ru": "<explanation>",
    "en": "<explanation>"
  }}
}}

📌 Additional Requirements:


- never same answer letter
- Subject must be "matematika" — not chemistry or any other subject.
- Topic must reflect the actual question content.
- Translations must be complete and accurate — do not omit numbers, formulas, or key terms.
- All option values must be wrapped in LaTeX-style math format: `$...$`
- Final answer must match one of the options.
- Solutions must include both methods with clear steps and final answers.
- Explanation must be readable, relevant, and match the question.
- Do not generate vague, incomplete, or repetitive content.
- Do not include any commentary or extra text outside the JSON array.

🚨 Mandatory Answer Diversity Rule:

- You must ensure that the correct answer letter ("answer" field) is different across clones. Do not assign the same answer letter (e.g., "A") to multiple clones in a row.
- The answer letter must rotate across clones (e.g., A, B, C, D) in a randomized but non-repetitive way.
- The "final_answer" must be placed under the correct option letter. For example, if the final answer is "$42$", and the answer is "C", then option "C" must contain "$42$" in all three languages.
- Do not mismatch the answer letter and its value. The answer must point to the option that contains the correct numeric value.
- Any clone that repeats the same answer letter as the previous clone is considered invalid.
- This rule is strict and non-negotiable. All clones must follow it.



📌 Answer Placement Rules:
- The correct answer must not always be assigned to the same option letter across clones. You must rotate the correct answer position (e.g., A, B, C, D) across different clones.
- The value of the correct answer must be placed under the correct option letter. Do not mismatch the answer letter and its value.
- Avoid repeating the same answer letter across multiple clones (e.g., do not use "A" as the answer for all 5 clones).
- Ensure that each clone has a unique and logically placed correct answer.

📌 Final Answer & Option Alignment Rules:
- You must solve the math problem correctly using valid mathematical reasoning. Do not fabricate or guess the final answer.
- The "final_answer" field must reflect the actual solution to the question — not a placeholder or reused value.
- The correct numeric value must be placed under the correct option letter. For example, if the final answer is "$135$", and the answer is "B", then option "B" must contain "$135$" in all three languages.
- Do not mismatch the answer letter and its value. The answer must point to the option that contains the correct value.
- All option values (A, B, C, D) must be distinct and mathematically plausible. Do not reuse the same values across clones.
- Do not use the same set of options repeatedly. Each clone must have a unique combination of options.
- The correct answer must vary across clones — do not assign the same answer letter (e.g., "A") to all clones.
- The solution steps must clearly explain how the final answer was derived, and must match the numeric result shown in the options.
- dont add another number to same the option
- The correct answer must not always be assigned to the same option letter (e.g., "A"). You must randomly assign the correct answer to different option letters across clones.
- The value of the correct answer must be placed under the correct option letter. For example, if the final answer is "$42$", and the answer is "C", then option "C" must contain "$42$" in all three languages.
- Do not mismatch the answer letter and its value. The "answer" field must point to the option that contains the correct numeric value.
- Each clone must have a unique combination of option values and answer placement. Avoid repeating the same answer letter or option set across clones.
- This rule is strict. Any mismatch between the final answer and the option values is considered invalid.

📌 Translation & Explanation Accuracy Rules:
- All translations in the "question" and "explanation" fields must be complete, accurate, and semantically correct in Uzbek, Russian, and English.
- Use meaningful and contextually appropriate vocabulary in each language. Avoid literal or broken translations.
- The "explanation" field must clearly describe how the problem was solved — including the reasoning, logic, and steps used to arrive at the final answer.
- Do not simply restate the final answer. The explanation must walk through the problem-solving process in a way that helps learners understand the method.
- Do not include unrelated or off-topic content in the explanation. It must be directly relevant to the question and its solution.
- The explanation must be clear, readable, and pedagogically useful in all three languages.


📌 Final Answer & Option Letter Matching Rule:
- The "final_answer" must be placed under the correct option letter. For example, if the final answer is "$7$", and it is located in option "A", then the "answer" field must be "A".
- Do not mismatch the answer letter and its value. The "answer" field must point to the option that contains the correct numeric value.
- You must verify that the final answer value and the selected answer letter are aligned correctly in every clone.
- This rule is mandatory. Any mismatch between the final answer and the answer letter is considered invalid.

🚨 Core Integrity Rule — Mandatory:
- You must never assign the same answer letter (e.g., "A") to multiple clones in a row. The correct answer must rotate across different option letters (e.g., A, B, C, D) to ensure diversity.
- The correct numeric value must always be placed under the correct option letter. For example, if the final answer is "$42$", and the answer is "C", then option "C" must contain "$42$" in all three languages.
- The "final_answer" must be the result of a valid and accurate solution. Do not fabricate or guess the answer.
- The "answer" field must always point to the option that contains the correct value. Any mismatch is considered invalid.
- You must never produce an incorrect answer. Every clone must solve the question correctly and place the correct result in the correct option.
- This rule is non-negotiable. Any violation of this rule invalidates the entire clone.


📌 Additional Cloning Rules:
- When generating clones, preserve the structure and meaning of the original question. Only change the numerical values in the problem — do not add extra context or unrelated content.
- All numerical values inside the question text must be wrapped in LaTeX-style math format: `$...$`.
- Do not repeat the same answer across multiple clones (e.g., avoid all answers being "A").
- Do not repeat identical option values across clones — each clone must have distinct options.
- The correct answer must always match the correct option letter (e.g., if the answer is "C", the correct value must be under option "C").
- The "steps" section in the solution must be fully explained in Uzbek — not just numeric calculations, but clear reasoning and commentary.
- The solution must be relevant to the question and logically complete.

Return only a valid JSON array of {n_clones} objects — no extra text, no commentary.

Output format:
[
  {{ clone1 }},
  {{ clone2 }},
  {{ clone3 }},
  {{ clone4 }},
  {{ clone5 }}
]
"""
    for attempt in range(max_retries):
        raw = ollama_generate(prompt)
        try:
            start = raw.index("[")
            end = raw.rindex("]") + 1
            parsed = json.loads(raw[start:end])
            if isinstance(parsed, list) and len(parsed) == n_clones:
                return parsed
            else:
                print(f"⚠️ Attempt {attempt+1}: Invalid clone count ({len(parsed)}), retrying...")
        except Exception as e:
            print(f"❌ Attempt {attempt+1}: JSON parsing error:", e)
            print("📄 Raw model output:\n", raw)
        time.sleep(2)  # brief pause before retry
    print("❌ Failed to generate valid clone set after retries.")
    return []

if __name__ == "__main__":
    # Load original questions
    with open("copy.json", "r", encoding="utf-8") as f:
        tasks = json.load(f)

    dataset = []
    for i, task in enumerate(tasks):
        print(f"🔄 Generating clones for question #{i+1}")
        clones = make_clones_with_llama(task, n_clones=5)
        if clones:
            dataset.extend(clones)
        else:
            print(f"⚠️ Skipped question #{i+1} due to generation error.")

    # Save final dataset
    with open("dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"✅ Dataset generated successfully with {len(dataset)} questions: dataset.json")
