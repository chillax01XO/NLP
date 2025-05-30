import spacy
import os
import random
import json

INPUT_DIR = "/Users/blooomyomg/PycharmProjects/PythonProject1/arxiv_cs/text"
OUTPUT_FILE = "ner_training_data.json"
# Сколько файлов максимум обрабатывать (чтобы не перегрузить)
MAX_DOCS = 50

# Загружаю стандартную английскую модель SpaCy
nlp = spacy.load("en_core_web_sm")
training_data = []

# Беру только .txt файлы из папки и перемешиваю — для разнообразия
files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
random.shuffle(files)

# Пробегаюсь по первым MAX_DOCS файлам
for filename in files[:MAX_DOCS]:
    with open(os.path.join(INPUT_DIR, filename), 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        doc = nlp(text)  # Прогоняю текст через NLP пайплайн
        entities = []
        for ent in doc.ents:
            # Беру только нужные типы сущностей: люди, организации и география
            if ent.label_ in ["PERSON", "ORG", "GPE"]:
                entities.append((ent.start_char, ent.end_char, ent.label_))
        # Если что-то нашли — добавляем в тренировочные данные
        if entities:
            training_data.append((text, {"entities": entities}))

# Сохраняю всё в json-файл
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(training_data, f, indent=2)

print(f" Сохранено {len(training_data)} примеров в {OUTPUT_FILE}")