import spacy
import os
import csv

MODEL_PATH = "ner_model"
INPUT_DIR = "/Users/blooomyomg/PycharmProjects/PythonProject1/arxiv_cs/text"
OUTPUT_FILE = "ner_results.csv"

# Список всякого "мусора", который не считаю настоящими сущностями (стоп слова)
EXCLUDE_TERMS = {
    'al', 'al.', 'pp', 'fig', 'Fig', 'et', 'etc', 'i.e', 'e.g',
    'J.', 'Vol', 'No', 'vs'
}

# Загружаю свою обученную модель
nlp = spacy.load(MODEL_PATH)

# Открываю CSV на запись
with open(OUTPUT_FILE, mode="w", newline='', encoding="utf-8") as out_file:
    writer = csv.writer(out_file)
    writer.writerow(["filename", "entity", "label"])  # заголовки колонок

    # Прохожусь по всем .txt файлам в директории
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(INPUT_DIR, filename)
            with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
                text = f.read()
                doc = nlp(text)  # прогоняю текст через модель
                for ent in doc.ents:
                    entity_text = ent.text.strip()
                    # отбрасываю короткие и "мусорные" сущности
                    if len(entity_text) >= 3 and entity_text not in EXCLUDE_TERMS:
                        writer.writerow([filename, entity_text, ent.label_])  # пишу строку в CSV

print(f"Результат сохранён в: {OUTPUT_FILE}")