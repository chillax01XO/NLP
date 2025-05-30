import os
import string
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

TEXT_DIR = "/Users/blooomyomg/PycharmProjects/PythonProject1/Task_1/arxiv_cs/text"

# Убираю всё ненужное
stopwords = {
    'the', 'and', 'of', 'to', 'in', 'for', 'on', 'we', 'is', 'with', 'that', 'as',
    'this', 'by', 'are', 'from', 'or', 'an', 'our', 'each', 'be', 'can', 'which',
    'these', 'it', 'at', 'using', 'used', 'has', 'have', 'also', 'was', 'their',
    'a', 'not', 'more', 'such', 'than', 'between', 'may', 'been'
}

# Простой токенизатор: всё в нижний регистр, убираю знаки препинания
def tokenize(text):
    tokens = text.lower().split()
    return [token.strip(string.punctuation) for token in tokens if token.isalpha()]

all_tokens = []

# Пробегаюсь по всем .txt файлам и собираю токены
for filename in os.listdir(TEXT_DIR):
    if filename.endswith(".txt"):
        path = os.path.join(TEXT_DIR, filename)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            tokens = tokenize(text)
            # фильтрую всё короткое и стоп-слова
            filtered = [t for t in tokens if t not in stopwords and len(t) > 2]
            all_tokens.extend(filtered)

# Считаю, сколько раз каждое слово встретилось
freq = Counter(all_tokens)

# Генерирую облако слов
wc = WordCloud(width=1200, height=600, background_color='white')
wc.generate_from_frequencies(freq)

# Сохраняю в файл
wc.to_file("terms_cloud.png")
print("Облако терминов сохранено в terms_cloud.png")

plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()