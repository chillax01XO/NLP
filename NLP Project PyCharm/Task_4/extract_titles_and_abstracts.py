import os
import pandas as pd

TEXT_DIR = "/Users/blooomyomg/PycharmProjects/PythonProject1/Task_1/arxiv_cs/text"

# Пытаюсь вытащить заголовок и аннотацию из текста
def extract_title_and_abstract(text):
    lines = text.strip().split("\n")
    lines = [line.strip() for line in lines if line.strip()]  # убираю пустые строки и лишние пробелы

    title = ""
    # Предполагаю, что заголовок — это короткая строка без точки, в начале файла
    for line in lines[:5]:
        if len(line.split()) <= 20 and '.' not in line:
            title = line
            break

    abstract = ""
    # Ищу аннотацию — ориентируюсь на типичные начала
    for i, line in enumerate(lines):
        l = line.lower()
        if any(l.startswith(start) for start in ["abstract", "this paper", "we present", "in this paper"]):
            abstract = lines[i]
            # Если аннотация совсем короткая, добавляю ещё строку (может быть продолжение)
            if len(abstract) < 50 and i + 1 < len(lines):
                abstract += " " + lines[i + 1]
            break

    return title.strip(), abstract.strip()

# Сюда собираю результат по всем файлам
results = []

# Пробегаюсь по каждому .txt файлу и вытаскиваю заголовок + аннотацию
for filename in os.listdir(TEXT_DIR):
    if filename.endswith(".txt"):
        path = os.path.join(TEXT_DIR, filename)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            title, abstract = extract_title_and_abstract(text)
            results.append({
                "Файл": filename,
                "Заголовок": title,
                "Аннотация": abstract
            })


df = pd.DataFrame(results)
output_path = "summary_table.csv"
df.to_csv(output_path, index=False)
print(f"\nСохранено: {output_path}")