import os
import sys
import json
from reader.pdf_reader import extract_pdf_text
from reader.docx_reader import extract_docx_text
from parser.leaflet_splitter import split_into_leaflets
from extractor.extract_fields import extract_fields_leaflet, extract_fields_fda


def read_text_from_file(path):
    """
    Detects file type (.pdf or .docx) and extracts raw text accordingly.
    """
    if path.endswith(".pdf"):
        return extract_pdf_text(path)
    elif path.endswith(".docx"):
        return extract_docx_text(path)
    else:
        raise ValueError("Unsupported file type. Please use a .pdf or .docx file.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py path_to_file")
        sys.exit(1)

    file_path = sys.argv[1]
    full_text = read_text_from_file(file_path)
    leaflets = split_into_leaflets(full_text)  # Split document into individual leaflets

    os.makedirs("output", exist_ok=True)

    for i, leaflet_text in enumerate(leaflets):
        # Detect format and extract fields accordingly
        if "Package leaflet: Information for the user" in leaflet_text:
            result = extract_fields_leaflet(leaflet_text)
        elif "MEDICATION GUIDE" in leaflet_text:
            result = extract_fields_fda(leaflet_text)
        else:
            print(f"❗ Skipped leaflet {i+1}: unknown format")
            continue

        # Save extracted fields to JSON
        with open(f"output/leaflet_{i+1}.json", "w") as f:
            json.dump(result, f, indent=2)

    print(f"✅ Extracted {len(leaflets)} leaflets → saved in output/")