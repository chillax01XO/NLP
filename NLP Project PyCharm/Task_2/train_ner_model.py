import spacy
import random
import json
from pathlib import Path
from spacy.training.example import Example

TRAINING_DATA_PATH = "ner_training_data.json"
OUTPUT_DIR = "ner_model"

N_ITER = 20  # сколько раз гонять обучение

# Загружаю базовую английскую модель SpaCy
nlp = spacy.load("en_core_web_sm")
ner = nlp.get_pipe("ner")  # достаю пайплайн для NER

# Загружаю данные, которые до этого сгенерил из статей
with open(TRAINING_DATA_PATH, "r", encoding="utf-8") as f:
    training_data = json.load(f)

# Добавляю в модель все сущности, которые есть в датасете
for _, annotations in training_data:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Превращаю сырые данные в spaCy-шные примеры
examples = []
for text, annotations in training_data:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annotations)
    examples.append(example)

# Отключаю всё, кроме NER (чтобы обучалась только Named Entity Recognition часть)
disabled = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*disabled):
    optimizer = nlp.resume_training()  # старт/продолжение обучения
    for itn in range(N_ITER):
        print(f"Итерация {itn + 1}/{N_ITER}")
        random.shuffle(examples)  # перемешал, чтобы модель не привыкала к порядку
        losses = {}
        for batch in spacy.util.minibatch(examples, size=4):
            nlp.update(batch, drop=0.3, losses=losses)  # немного дропаут, чтобы не переучивалась
        print(f"Потери: {losses['ner']:.4f}")  # просто смотрю, как идут потери


output_dir = Path(OUTPUT_DIR)
output_dir.mkdir(exist_ok=True)
nlp.to_disk(output_dir)
print(f"\nМодель сохранена в: {OUTPUT_DIR}")