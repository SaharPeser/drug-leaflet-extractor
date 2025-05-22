import re

def split_sections(leaflet_text):
    """
    Splits a single leaflet into sections based on numbered or capitalized headers.
    Returns a dictionary of {section_title: section_content}
    """
    pattern = r"\n\s*(\d{1,2}\.\s+.*?|[A-Z ]{5,})\s*\n"
    matches = list(re.finditer(pattern, leaflet_text))
    sections = {}

    for i in range(len(matches)):
        title = matches[i].group(1).strip()
        start = matches[i].end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(leaflet_text)
        content = leaflet_text[start:end].strip()
        sections[title] = content

    return sections
