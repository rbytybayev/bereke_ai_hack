from langdetect import detect

def detect_language(text: str) -> str:
    try:
        lang = detect(text[:1000])
        return lang
    except:
        return "unknown"
