from japanese_crossword.helpers import find_first_1_index, find_last_1_index


def test__find_last_1_index__returns_correct_index_for_complex_input():
    assert find_last_1_index([None, 1, 1, None, None, 1, 1, 1, 1, 1, None]) == 9


def test__find_last_1_index__returns_correct_index_for_just_one_1():
    assert find_last_1_index([1]) == 0


def test__find_last_1_index__returns_correct_index_for_several_1():
    assert find_last_1_index([1, 1, 1, 1, 1]) == 4


def test__find_last_1_index__returns_minus_one():
    assert find_last_1_index([None, None]) == -1


def test__find_first_1_index__returns_correct_index_for_complex_input():
    assert find_first_1_index([None, 1, 1, None, None, 1]) == 1


def test__find_first_1_index__returns_correct_index_for_just_one_1():
    assert find_first_1_index([1]) == 0


def test__find_first_1_index__returns_correct_index_for_several_1():
    assert find_first_1_index([1, 1, 1]) == 0


def test__find_first_1_index__returns_minus_one():
    assert find_first_1_index([None, None]) == -1
