from typing import Literal


def find_last_1_index(row: list[Literal[0, 1] | None]) -> int:
    for index, value in enumerate(reversed(row)):
        if value == 1:
            return len(row) - index - 1
    return -1


def find_first_1_index(row: list[Literal[0, 1] | None]) -> int:
    for index, value in enumerate(row):
        if value == 1:
            return index
    return -1
