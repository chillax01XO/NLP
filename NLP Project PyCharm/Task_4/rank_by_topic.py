import os
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


TEXT_DIR = "/Users/blooomyomg/PycharmProjects/PythonProject1/Task_1/arxiv_cs/text"
TOP_N = 10  # Сколько топовых результатов выводить

# Спрашиваю у пользователя, что он хочет найти
query = input("Введите ключевую тему для поиска статей: ").strip()

# Привожу запрос к виду, который можно использовать в имени файла
filename_safe_query = re.sub(r'\W+', '_', query.lower())
output_file = f"relevant_articles_{filename_safe_query}.csv"

# Собираю все тексты и имена файлов
documents = []
filenames = []
for filename in os.listdir(TEXT_DIR):
    if filename.endswith(".txt"):
        filepath = os.path.join(TEXT_DIR, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            documents.append(text)
            filenames.append(filename)

# Векторизую тексты с помощью TF-IDF
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.8)
doc_vectors = vectorizer.fit_transform(documents)
query_vector = vectorizer.transform([query])  # Векторизую сам запрос

# Считаю косинусное сходство между запросом и каждым документом
similarities = cosine_similarity(query_vector, doc_vectors).flatten()
top_indices = similarities.argsort()[::-1][:TOP_N]  # Беру топ-N самых похожих

# Формирую таблицу с результатами
results = []
for idx in top_indices:
    frag = documents[idx][:300].replace("\n", " ")  # Показываю кусочек текста
    results.append({
        "Файл": filenames[idx],
        "Сходство": round(similarities[idx], 3),
        "Фрагмент": frag
    })

# Сохраняю таблицу в CSV
df = pd.DataFrame(results)
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"\nСохранено в файл: {output_file}")