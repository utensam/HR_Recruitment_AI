import fitz  # PyMuPDF for PDFs
import docx  # python-docx for Word files
import spacy


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def extract_text_from_docx(docx_path):
    """Extracts text from a Word document."""
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text


def extract_skills_and_experience(text):
    """Uses NLP to extract skills and experience from resume text."""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    skills = []  # Placeholder for actual skill extraction
    experience = []

    for ent in doc.ents:
        if ent.label_ in ["ORG", "WORK_OF_ART", "PRODUCT"]:  # Adjust labels as needed
            skills.append(ent.text)
        if ent.label_ in ["DATE", "TIME", "CARDINAL"]:
            experience.append(ent.text)

    return set(skills), set(experience)


# Example usage
if __name__ == "__main__":
    pdf_text = extract_text_from_pdf("sample_resume.pdf")
    docx_text = extract_text_from_docx("sample_resume.docx")

    combined_text = pdf_text + docx_text
    skills, experience = extract_skills_and_experience(combined_text)

    print("Skills:", skills)
    print("Experience:", experience)
