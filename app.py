import re
import json

def clean_text(text):
    # Remove trailing LaTeX line breaks (\\) and strip spaces/newlines
    return re.sub(r'\\\\$', '', text.strip())

# Step 1: Load raw LaTeX content from birinchi_qism.tex
with open("Kimyo_noldan_1.tex", "r", encoding="utf-8") as f:
    data = f.read()

# Step 2: Split questions by \item or numbered lines like 55.
question_blocks = re.split(r'(?:\\item|\n\s*\d{1,3}\.)', data)
question_blocks = [q.strip() for q in question_blocks if q.strip()]

questions = []
question_number = 1

for block in question_blocks:
    # Match options A) B) C) D) with flexible whitespace/newlines between them
    option_match = re.search(
        r'A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*)', block, re.DOTALL)

    if option_match:
        # Extract question text (everything before "A)")
        question_text = clean_text(re.split(r'A\)', block)[0])

        # Detect if images exist and get image file names
        has_image = '\\includegraphics' in block
        images = re.findall(r'\\includegraphics(?:\[.*?\])?\{(.*?)\}', block)

        options = {
            "A": clean_text(option_match.group(1)),
            "B": clean_text(option_match.group(2)),
            "C": clean_text(option_match.group(3)),
            "D": clean_text(option_match.group(4))
        }

        questions.append({
            "number": question_number,
            "question": question_text,
            "has_image": has_image,
            "images": images,
            "options": options
        })

        question_number += 1

# Step 3: Write parsed questions to JSON
with open("parsed_questions.json", "w", encoding="utf-8") as out_file:
    json.dump(questions, out_file, ensure_ascii=False, indent=2)

print(f"✅ Parsed {len(questions)} questions into 'parsed_questions.json'")
