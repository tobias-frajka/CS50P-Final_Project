import pytest, string
from project import parse_arguments, generate_password, get_subset, generate_special_password # type: ignore

def test_parser():
    args = ["10", "-t", "0"]
    result = parse_arguments(args)
    assert result.length == 10
    assert result.type == 0
    assert result.uppercase == None

    args = ["52", "-t", "3", "-u", "4", "-n", "5", "-c", "4", "-s", "3"]
    result = parse_arguments(args)
    assert result.length == 52
    assert result.type == 3
    assert result.uppercase == 4
    assert result.numbers == 5
    assert result.characters == 4
    assert result.save == 3

    args = ["101", "-t", "3"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)

    args = ["-1", "-t", "3"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)

    args = ["10", "-t", "4"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)

    args = ["10", "-t", "3", "-u"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)

    args = ["-t", "3"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)

    args = ["10", "-t", "3", "-u", "11"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)

    args = ["10", "-t", "3", "-u", "5", "-c", "6"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)

    args = ["10", "-t", "0", "-u", "5"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)

    args = ["10", "-t", "0", "-s"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)

    args = ["10", "-t", "0", "-s", "-1"]
    with pytest.raises(SystemExit):
        result = parse_arguments(args)


def test_subset():
    subset = get_subset(0)
    assert subset == string.digits

    subset = get_subset(1)
    assert subset == string.ascii_letters

    subset = get_subset(2)
    assert subset == string.digits + string.ascii_letters

    subset = get_subset(3)
    assert subset == string.digits + string.ascii_letters + string.punctuation

    with pytest.raises(ValueError):
        subset = get_subset(4)

        subset = get_subset(string.digits)

        subset = get_subset(-1)


def test_generate_password():
    result = generate_password(10, string.ascii_letters)

    assert len(result) == 10
    assert all(not char.isdigit() for char in result)

    result = generate_password(50, string.digits)

    assert len(result) == 50
    assert all(char.isdigit() for char in result)

def test_generate_special_password():
    requirements = {
                "uppercase": None,
                "numbers": 5,
                "characters": None,
                }

    result = generate_special_password(10, requirements, string.ascii_letters + string.digits)

    assert len(result) == 10

    digit_count = sum(1 for digit in result if digit.isdigit())
    assert digit_count == 5

    requirements = {
                "uppercase": 4,
                "numbers": 5,
                "characters": 5,
                }

    result = generate_special_password(15, requirements, string.ascii_letters + string.digits)

    assert len(result) == 15

    digit_count = sum(1 for digit in result if digit.isdigit())
    assert digit_count == 5

    char_count = sum(1 for char in result if char in string.punctuation)
    assert char_count == 5

    upper_count = sum(1 for char in result if char.isupper())
    assert upper_count == 4



