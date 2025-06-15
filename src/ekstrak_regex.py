import fitz
import re
import json
import os

def extract_regex(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        print(f"Error: File tidak ditemukan di '{pdf_path}'")
        return ""
    try:
        doc = fitz.open(pdf_path)
        raw_text = "".join(page.get_text("text") for page in doc)
        doc.close()
        
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,\-+:/&]', '', raw_text)
        
        lines = cleaned_text.split('\n')
        stripped_lines = [line.strip() for line in lines]
        final_text = "\n".join(stripped_lines)
        return final_text
    except Exception as e:
        print(f"Gagal membaca PDF {os.path.basename(pdf_path)}: {e}")
        return ""

def extract_details_regex(cv_text: str) -> dict:
    details = {
        "summary": [],
        "skills": [],
        "experience": [],
        "education": []
    }

    def clean_list(items):
        return [item.strip() for item in items if item.strip()]

    summary_match = re.search(r'(?ism)^Summary\s*\n([\s\S]+?)(?=\n(?:Skills|Experience|Education|Highlights|Accomplishments)\n|\Z)', cv_text)
    if summary_match:
        details["summary"] = clean_list(summary_match.group(1).split('\n'))

    skills_match = re.search(r'(?ism)^Skills\s*\n([\s\S]+?)(?=\n(?:Summary|Experience|Education|Highlights|Accomplishments)\n|\Z)', cv_text)
    if skills_match:
        details["skills"] = clean_list(skills_match.group(1).split('\n'))

    exp_match = re.search(r'(?ism)^Experience\s*\n([\s\S]+?)(?=\nEducation\n|\Z)', cv_text)
    if exp_match:
        experience_block = exp_match.group(1).strip()
        
        entries = re.findall(
            r'(?m)^(\d{2}/\d{4}.*?)\n(.*?)\n([\s\S]+?)(?=(?:\n\d{2}/\d{4})|\Z)',
            experience_block
        )
        
        for entry in entries:
            periode, info_jabatan, deskripsi_block = entry
            details["experience"].append({
                "periode": periode.strip(),
                "info_jabatan": info_jabatan.strip(),
                "deskripsi": clean_list(deskripsi_block.split('\n'))
            })

    edu_match = re.search(r'(?ism)^Education\s*\n([\s\S]+)', cv_text)
    if edu_match:
        education_block = edu_match.group(1).strip()
        details["education"] = clean_list(education_block.split('\n'))
        
    return details

if __name__ == "__main__":
    cv_pdf_path = "10276858.pdf"
    
    print(f"Mengekstrak detail dari: '{cv_pdf_path}'")

    cleaned_cv_text = extract_regex(cv_pdf_path)

    if cleaned_cv_text:
        structured_data = extract_details_regex(cleaned_cv_text)

        print("\nSummary CV")
        print(json.dumps(structured_data, indent=4))
    else:
        print("Gagal mendapatkan teks dari PDF.")