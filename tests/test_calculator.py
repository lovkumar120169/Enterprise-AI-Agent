import pytest

from backend.tools.calculator import calculate


def test_addition():
    result = calculate("2 + 3")

    assert result["result"] == 5


def test_complex_expression():
    result = calculate("(10 + 5) * 2")

    assert result["result"] == 30


def test_power():
    result = calculate("2 ** 3")

    assert result["result"] == 8


def test_negative_number():
    result = calculate("-10 + 5")

    assert result["result"] == -5


def test_expression_too_long():
    expression = "1" * 201

    with pytest.raises(ValueError, match="Expression is too long"):
        calculate(expression)


def test_invalid_operator():
    with pytest.raises(ValueError):
        calculate("2 // 2")


def test_non_numeric_expression():
    with pytest.raises(ValueError):
        calculate("'hello'")