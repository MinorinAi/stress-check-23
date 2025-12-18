# tests/test_scoring.py
import pytest
from scoring import evaluate, classify_level, compute_totals

def full_answers(value: int = 1):
    return {i: value for i in range(1, 24)}

def test_totals_all_ones():
    ans = full_answers(1)
    A, B = compute_totals(ans)
    assert A == 11
    assert B == 12

def test_level_rule_low_B_branch():
    # B_total<=38 の分岐をチェック
    assert classify_level(15, 38) == "Ⅰ"
    assert classify_level(16, 38) == "Ⅱ"
    assert classify_level(30, 38) == "Ⅱ"
    assert classify_level(31, 38) == "Ⅲ"

def test_level_rule_high_B_branch():
    # B_total>38 の分岐をチェック
    assert classify_level(22, 39) == "Ⅱ"
    assert classify_level(23, 39) == "Ⅲ"

def test_missing_answers_raises():
    ans = full_answers(1)
    ans.pop(23)
    with pytest.raises(ValueError):
        evaluate(ans)

def test_out_of_range_raises():
    ans = full_answers(1)
    ans[5] = 5
    with pytest.raises(ValueError):
        evaluate(ans)
