import os
import string
import csv
from collections import Counter
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

TEXT_DIR = "/Users/blooomyomg/PycharmProjects/PythonProject1/Task_1/arxiv_cs/text"

# Свой список стоп-слов — выкидываю лишнее, чтобы не мешалось
custom_stopwords = {
    'the', 'and', 'of', 'to', 'in', 'for', 'on', 'we', 'is', 'with', 'that', 'as',
    'this', 'by', 'are', 'from', 'or', 'an', 'our', 'each', 'be', 'can', 'which',
    'these', 'it', 'at', 'using', 'used', 'has', 'have', 'also', 'was', 'their',
    'not', 'more', 'all', 'such', 'than', 'may', 'one', 'two', 'three', 'four'
}

# Простая токенизация: привожу к нижнему регистру, убираю знаки препинания
def tokenize(text):
    tokens = text.lower().split()
    return [token.strip(string.punctuation) for token in tokens if token.isalpha()]

all_tokens = []

# Читаю все .txt файлы и собираю токены
for filename in os.listdir(TEXT_DIR):
    if filename.endswith(".txt"):
        filepath = os.path.join(TEXT_DIR, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            tokens = tokenize(text)
            all_tokens.extend(tokens)

# Убираю стоп-слова и короткие токены
filtered_tokens = [t for t in all_tokens if t not in custom_stopwords and len(t) > 2]

# Частотный список слов (unigrams), беру топ-100
unigram_freq = Counter(filtered_tokens)
top_unigrams = unigram_freq.most_common(100)

# Считаю биграммы и сортирую по T-score, беру топ-100
finder = BigramCollocationFinder.from_words(filtered_tokens)
bigram_scores = finder.score_ngrams(BigramAssocMeasures().student_t)
top_bigrams = sorted(bigram_scores, key=lambda x: -x[1])[:100]

# Просто вывожу в консоль
print("\nТОП-100 однословных терминов:")
for term, freq in top_unigrams:
    print(f"{term:20} {freq}")

print("\nТОП-100 двусловных терминов по T-score:")
for (w1, w2), score in top_bigrams:
    print(f"{w1} {w2:20} {score:.2f}")

# Сохраняю всё в CSV-файл
output_path = "terms_top100.csv"
with open(output_path, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Term", "Score"])
    for term, freq in top_unigrams:
        writer.writerow([term, freq])
    for (w1, w2), score in top_bigrams:
        writer.writerow([f"{w1} {w2}", f"{score:.2f}"])

print(f"\nРезультаты сохранены в {output_path}")