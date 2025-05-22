import re

def split_into_leaflets(text):
    """
    Splits the full document into separate leaflets using known headers
    (EMA: 'Package leaflet: Information for the user')
    (FDA: 'MEDICATION GUIDE')
    """
    # Match both EMA and FDA styles
    pattern = r"(Package leaflet: Information for the user|MEDICATION GUIDE)"
    matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))

    leaflets = []
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        leaflet = text[start:end].strip()
        leaflets.append(leaflet)

    return leaflets
