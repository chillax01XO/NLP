import feedparser
import requests
import os
from PyPDF2 import PdfReader
import time

# Задаю папки, где будут храниться PDF и текст
BASE_DIR = "arxiv_cs"
PDF_DIR = os.path.join(BASE_DIR, "pdf")
TXT_DIR = os.path.join(BASE_DIR, "text")

# Создаю папки, если их нет — чтобы не падало при запуске
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(TXT_DIR, exist_ok=True)

# URL для API arXiv и нужная категория (AI)
BASE_URL = "http://export.arxiv.org/api/query?"
CATEGORY = "cs.AI"
BATCH_SIZE = 100  # Сколько статей запрашивать за раз

# Функция, чтобы получать список статей из arXiv
def fetch_entries(start=0, max_results=100):
    query = f"search_query=cat:{CATEGORY}&start={start}&max_results={int(max_results)}&sortBy=submittedDate&sortOrder=descending"
    feed_url = BASE_URL + query
    feed = feedparser.parse(feed_url)
    return feed.entries

# Качаем PDF по ссылке и сохраняем в файл
def download_pdf(url, filename):
    try:
        r = requests.get(url, timeout=20)
        with open(filename, 'wb') as f:
            f.write(r.content)
        return True
    except Exception as e:
        print(f"Ошибка при скачивании PDF: {e}")
        return False

# Извлекаем текст из PDF-файла
def extract_text_from_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        text = ''
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t
        return text
    except Exception as e:
        print(f"Ошибка при извлечении текста: {e}")
        return ''

# Скачиваем статьи, сохраняем тексты, пока не наберётся нужный объём
def main():
    total_text = ''
    article_count = 0
    start = 0

    # Пока не набрали примерно 12 МБ текста (ограничение)
    while len(total_text.encode('utf-8', errors='ignore')) < 12 * 1024 * 1024:
        print(f"Получаем статьи {start}–{start + BATCH_SIZE}...")
        entries = fetch_entries(start, BATCH_SIZE)
        if not entries:
            print("Больше статей не найдено.")
            break
        for entry in entries:
            arxiv_id = entry.get("id").split("/")[-1]
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            pdf_filename = os.path.join(PDF_DIR, f"article_{article_count}.pdf")
            txt_filename = os.path.join(TXT_DIR, f"article_{article_count}.txt")

            print(f"Скачиваем PDF: {pdf_url}")
            if download_pdf(pdf_url, pdf_filename):
                text = extract_text_from_pdf(pdf_filename)
                if text:
                    # Сохраняю текст в отдельный файл
                    with open(txt_filename, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(text)
                    total_text += text
                    size_mb = len(total_text.encode('utf-8', errors='ignore')) / (1024 * 1024)
                    print(f"Всего: {size_mb:.2f} МБ")
                    article_count += 1
                    # Если превысили 15 МБ — выходим досрочно
                    if size_mb >= 15:
                        break
        start += BATCH_SIZE
        time.sleep(1)  # Немного подождать между запросами, чтобы не спамить

    # Финальная инфа: сколько скачали, сколько получилось текста
    final_size = len(total_text.encode('utf-8', errors='ignore')) / (1024 * 1024)
    print(f"\nСтатей: {article_count}, объём текста: {final_size:.2f} МБ")
    print(f"PDF-файлы: {PDF_DIR}")
    print(f"Тексты: {TXT_DIR}")

if __name__ == "__main__":
    main()