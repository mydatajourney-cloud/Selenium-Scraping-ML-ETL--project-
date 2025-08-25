import re
def normalize_email(text):
    patterns = {
        r"\(at\)|\[at\]|\{at\}|\bat\b|\(ät\)|\[ät\]|\{ät\}|\bät\b|\(AT\)|\[AT\]|\{AT\||\bAT\b": "@",
        r"\(dot\)|\[dot\]|\{dot\}|\bdot\b|\s+punkt\s+|\[punkt\]|\(punkt\)|\[punto\]|\s+DOT\s+": "."
    }

    normalized = text
    for pat, repl in patterns.items():
        normalized = re.sub(pat, repl, normalized, flags=re.IGNORECASE)

    # Loại bỏ khoảng trắng thừa nhưng giữ cấu trúc
    normalized = re.sub(r"\s+", "", normalized)
    # Xác thực email
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.findall(email_pattern, normalized)
    return match