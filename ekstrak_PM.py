import fitz
import re
import os

def extract_text_pm(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        print(f"Error: File tidak ditemukan di '{pdf_path}'")
        return ""

    try:
        doc = fitz.open(pdf_path)
        raw_text = "".join(page.get_text("text") for page in doc)
        doc.close()

        lower_text = raw_text.lower()

        linear_text = re.sub(r'[\n\t•]', ' ', lower_text)

        allowed_chars_text = re.sub(r'[^a-z0-9\s,.:+-]', '', linear_text)

        normalized_text = re.sub(r'\s+', ' ', allowed_chars_text).strip()

        return normalized_text

    except Exception as e:
        print(f"Terjadi error saat memproses file {pdf_path}: {e}")
        return ""

if __name__ == "__main__":
    cv_pdf_path = "10276858.pdf"

    print(f"Memproses file: '{cv_pdf_path}'")

    result_text = extract_text_pm(cv_pdf_path)

    if result_text:
        print("\Ekstrasi untuk PM:")
        print(result_text)
