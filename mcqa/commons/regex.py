import re
def extract_regex(text: str, pattern: str):
    """Extracts text using a given regex pattern."""
    return re.findall(pattern, text)