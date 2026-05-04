import re


def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500) -> list:
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def detect_document_type(text: str) -> str:
    lower_text = text.lower()

    invoice_keywords = ["fatura", "invoice", "tutar", "kdv", "vergi"]
    application_keywords = ["dilekçe", "başvuru", "talep", "sayın"]
    report_keywords = ["rapor", "analiz", "sonuç", "değerlendirme"]

    if any(word in lower_text for word in invoice_keywords):
        return "Fatura / Finansal Belge"

    if any(word in lower_text for word in application_keywords):
        return "Başvuru / Dilekçe"

    if any(word in lower_text for word in report_keywords):
        return "Rapor / Analiz Belgesi"

    return "Genel Doküman"


def analyze_document(text: str) -> dict:
    cleaned_text = clean_text(text)

    date_pattern = r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b"
    email_pattern = r"[\w\.-]+@[\w\.-]+"
    phone_pattern = r"\b05\d{2}\s?\d{3}\s?\d{2}\s?\d{2}\b"

    dates = re.findall(date_pattern, cleaned_text)
    emails = re.findall(email_pattern, cleaned_text)
    phones = re.findall(phone_pattern, cleaned_text)

    chunks = chunk_text(cleaned_text)

    return {
        "document_type": detect_document_type(cleaned_text),
        "character_count": len(cleaned_text),
        "word_count": len(cleaned_text.split()),
        "date_list": dates,
        "email_list": emails,
        "phone_list": phones,
        "chunk_count": len(chunks),
        "chunks": chunks
    }
