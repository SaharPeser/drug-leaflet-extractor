import re

# -------- EMA FORMAT (EUROPE) --------
def extract_fields_leaflet(text):
    """
    Extract fields from EMA-style patient leaflet.
    Sections: 1–4 are matched by number and title.
    """
    sections = {}

    section_titles = [
        ("indications", r"1\.\s*What .* is and what it is used for"),
        ("contraindications", r"2\.\s*What you need to know before you take .*"),
        ("dosage", r"3\.\s*How to take .*"),
        ("side_effects", r"4\.\s*Possible side effects")
    ]

    for i in range(len(section_titles)):
        field, start_pattern = section_titles[i]
        end_pattern = section_titles[i + 1][1] if i + 1 < len(section_titles) else r"5\."
        pattern = rf"{start_pattern}(.*?){end_pattern}"
        match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
        sections[field] = match.group(1).strip() if match else ""

    name_match = re.search(r"Package leaflet: Information for the user\s*\n+(.*?)\n", text)
    sections["drug_name"] = name_match.group(1).strip() if name_match else ""

    active_match = re.search(r"\bcontains\s+(clopidogrel|nivolumab)", text, re.IGNORECASE)
    sections["active_ingredient"] = active_match.group(1).strip() if active_match else ""

    return sections

# -------- FDA FORMAT (USA) --------
def extract_fields_fda(text):
    """
    Extract fields from FDA-style Medication Guide.
    Based on capitalized question-style headers.
    """
    sections = {}

    fda_patterns = {
        "drug_name": r"MEDICATION GUIDE\s*\n(.*?)\n",
        "indications": r"(?i)what is .*?\?\n(.*?)(?=\n[A-Z ]{3,})",
        "contraindications": r"(?i)what should i tell my doctor.*?\?\n(.*?)(?=\n[A-Z ]{3,})",
        "dosage": r"(?i)how should i (use|take) .*?\?\n(.*?)(?=\n[A-Z ]{3,})",
        "side_effects": r"(?i)what are the possible side effects.*?\?\n(.*?)(?=\n[A-Z ]{3,})"
    }

    for field, pattern in fda_patterns.items():
        match = re.search(pattern, text, flags=re.DOTALL)
        if match:
            sections[field] = match.group(1).strip()
        else:
            sections[field] = ""

    active_match = re.search(r"\bcontains\s+(clopidogrel|nivolumab)", text, re.IGNORECASE)
    sections["active_ingredient"] = active_match.group(1).strip() if active_match else ""

    return sections
