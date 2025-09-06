import streamlit as st
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama2"

def generate_clones(question, n=5):
    prompt = f"""
    Ты генератор тестов.
    Вот вопрос: {json.dumps(question, ensure_ascii=False)}
    Сгенерируй {n} новых клонов в таком же JSON-формате.
    Ответь строго массивом JSON.
    """

    resp = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt}, stream=True)

    output = ""
    for line in resp.iter_lines():
        if line:
            try:
                data = json.loads(line)
                if "response" in data:
                    output += data["response"]
            except:
                continue

    output = output.strip()
    if output.startswith("```"):
        output = output.split("```")[1]
    output = output.strip("` \n")

    try:
        clones = json.loads(output)
        return clones
    except Exception as e:
        st.error(f"Ошибка парсинга JSON: {e}")
        st.code(output[:500])
        return []

st.title("Генератор клонов вопросов (Ollama)")

uploaded_file = st.file_uploader("Загрузите JSON с вопросами", type=["json"])

num_clones = st.number_input("Количество клонов на вопрос", min_value=1, max_value=20, value=5, step=1)

if uploaded_file:
    questions = json.load(uploaded_file)
    st.success(f"Загружено {len(questions)} вопросов!")

    if st.button("Сгенерировать клоны"):
        all_data = []
        progress_bar = st.progress(0)

        for idx, q in enumerate(questions):
            st.write(f"Обрабатываю вопрос №{q['number']}...")
            all_data.append(q)
            clones = generate_clones(q, n=num_clones)
            if clones:
                all_data.extend(clones)
            progress_bar.progress((idx + 1) / len(questions))

        st.success("✅ Генерация завершена!")

        # Сохраняем в файл для скачивания
        json_str = json.dumps(all_data, ensure_ascii=False, indent=2)
        st.download_button(
            label="Скачать все вопросы с клонами",
            data=json_str,
            file_name="questions_with_clones.json",
            mime="application/json"
        )
