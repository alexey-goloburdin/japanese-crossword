from typing import Literal


def find_last_1_index(row: list[Literal[1] | Literal[0] | None]) -> int:
    for index, value in enumerate(reversed(row)):
        if value == 1:
            return len(row) - index - 1
    return -1


def find_first_1_index(row: list[Literal[1] | Literal[0] | None]) -> int:
    for index, value in enumerate(row):
        if value == 1:
            return index
    return -1



if __name__ == "__main__":
    assert find_last_1_index([None, 1, 1, None, None, 1, 1, 1, 1, 1, None]) == 9
    assert find_last_1_index([1]) == 0
    assert find_last_1_index([None, 1]) == 1
    assert find_last_1_index([None, None]) == -1

    assert find_first_1_index([None, 1]) == 1
    assert find_first_1_index([None, 1, 1, 1]) == 1
    assert find_first_1_index([1, 1, 1]) == 0
    assert find_first_1_index([None, None, None, 1, 1, 1]) == 3
    assert find_first_1_index([None]) == -1

