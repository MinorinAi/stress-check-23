# scoring.py
from dataclasses import dataclass

COMMENTS = {
    "Ⅰ": "ストレスは軽度です。仕事や生活への影響は少ない状態です。",
    "Ⅱ": "中程度のストレスがあります。疲労がありつつも仕事を続けられています。",
    "Ⅲ": "高ストレス状態です。健康や業務に支障をきたす恐れがあります。"
}

@dataclass(frozen=True)
class StressResult:
    A_total: int
    B_total: int
    level: str
    comment: str

def validate_answers(answers: dict[int, int]) -> None:
    if set(answers.keys()) != set(range(1, 24)):
        raise ValueError("設問1〜23が揃っていません")
    for v in answers.values():
        if not isinstance(v, int) or not (1 <= v <= 4):
            raise ValueError("回答は1〜4の整数である必要があります")

def compute_totals(answers: dict[int, int]) -> tuple[int, int]:
    validate_answers(answers)
    A_total = sum(answers[i] for i in range(1, 12))
    B_total = sum(answers[i] for i in range(12, 24))
    return A_total, B_total

def classify_level(A_total: int, B_total: int) -> str:
    if B_total <= 38:
        return "Ⅰ" if A_total <= 15 else "Ⅱ" if A_total <= 30 else "Ⅲ"
    return "Ⅱ" if A_total <= 22 else "Ⅲ"

def evaluate(answers: dict[int, int]) -> StressResult:
    A_total, B_total = compute_totals(answers)
    level = classify_level(A_total, B_total)
    return StressResult(A_total, B_total, level, COMMENTS[level])
