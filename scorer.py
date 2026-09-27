import gate
import re

def _normalize(text: str) -> str: 
    text = text.strip().lower()
    text = re.sub(r"[^\w\s]", " ", text)   # strip punctuation, keep words
    text = re.sub(r"\s+", " ", text)
    return text

def _group_matches(group: str, answer: str) -> bool:
    alternatives = [_normalize(a) for a in group.split("|") if a.strip()]
    return any(alt in answer for alt in alternatives)

def judge(question: str, expects: str, answer: str, results: list) -> bool:
    if not expects:
        return None
    if answer.strip() == gate.REFUSAL.strip():
        return False
    answer = _normalize(answer)
    groups = [g.strip() for g in expects.split(" AND ") if g.strip()]
    return all(_group_matches(group, answer) for group in groups)