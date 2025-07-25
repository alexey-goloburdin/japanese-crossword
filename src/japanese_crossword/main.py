import json
import math
import sys
from pathlib import Path
from typing import Literal

from japanese_crossword import helpers


def read_crossword_rules(rules_file: str):
    try:
        return json.loads(Path(rules_file).read_text())
    except:
        sys.exit(f"Не удалось считать правила кроссворда из файла {rules_file}")


class IncorrectCellFill(Exception):
    """Неудачная попытка перевести статус клеточки в 0 или 1"""


type BoardRowState = list[Literal[0, 1] | None]
type BoardState = list[BoardRowState]


class Board:
    """
    Координаты верхнего левого угла: (0, 0)
    Координаты правого нижнего угла: (max_x - 1, max_y - 1)
    """

    render_values = {
        # "\033[2m" + "Тусклый текст" + "\033[0m"
        None: "\033[2m◌\033[0m ",  # неизвестно
        1: "\033[32m■\033[00m ",  # закрашено
        0: "\033[2m‧\033[0m ",  # не закрашено
    }

    def __init__(self, max_x: int, max_y: int):
        self._max_x = max_x
        self._max_y = max_y
        # В self._board храним массив строк
        self._board: BoardState = [[None for _ in range(max_x)] for _ in range(max_y)]

    def get_size(self):
        """
        Возвращает размер поля в формате (x, y).
        """
        return self._max_x, self._max_y

    def get_state(self) -> BoardState:
        """
        Возвращает копию текущего состояния поля — массив строк.
        """
        return list(self._board)

    def fill_cell(self, row: int, column: int, value: Literal[0, 1]):
        """
        Проставляет ячейку заполненной или пустой.
        """
        old_cell_value = self._board[row][column]
        if old_cell_value is not None and old_cell_value != value:
            raise IncorrectCellFill(
                f"Статус ячейки ({row}, {column}) был {old_cell_value}, нельзя перевести в {value}"
            )
        self._board[row][column] = value

    def print(self):
        """
        Печатает текущее состояние поля.
        """
        self._print_column_numbers_header()
        for row_number, row in enumerate(self._board, 1):
            self._print_row_header(row_number)
            for value in row:
                print(self.render_values[value], end="")
            self._print_row_header(row_number)
            print()
        self._print_column_numbers_header()

        print(f"Заполнено {self.get_filled_percent()}%")

    def get_filled_percent(self) -> int:
        overall_cells = self._max_x * self._max_y
        filled = 0
        for row in self._board:
            for value in row:
                if value is not None:
                    filled += 1
        return math.floor(100 * filled / overall_cells)

    def _print_column_numbers_header(self):
        print("   ", end="")
        for column_index in range(1, self._max_x + 1):
            if column_index in (1, 5):
                print(f"{column_index} ", end="")
            elif column_index % 5 == 0:
                print(column_index, end="")
            else:
                print("  ", end="")
        print()

    def _print_row_header(self, row_number: int):
        if row_number in (1, 5):
            print(f"{row_number}  ", end="")
        elif row_number % 5 == 0:
            print(f"{row_number} ", end="")
        else:
            print("   ", end="")


def _find_sausages_possible_edge_variants(rules, board_size):
    """
    Возвращает «крайние» варианты всех колбасок, если бы они начинались с самого левого или самого правого края для
    строк, и с самого верхнего или самого нижнего края для колонок.
    """
    sausages_variants_in_rows = []  # список строк или колонок с гипотетическими крайними положениями колбасок
    for rule_row in rules:
        # гипотетические положения колбасок в текущей строке
        sausages_variants_in_row = {
            sausage_index: {
                "start_variant_coords": tuple(),
                "end_variant_coords": tuple(),
            }
            for sausage_index in range(len(rule_row))
        }

        # Строим левый (от начала строки/колонки) вариант колбас
        current_cell_index = 0
        for sausage_index, sausage_length_rule in enumerate(rule_row):
            sausage_start_cell = current_cell_index
            sausage_end_cell = current_cell_index + sausage_length_rule - 1

            sausages_variants_in_row[sausage_index]["start_variant_coords"] = (
                sausage_start_cell,
                sausage_end_cell,
            )
            current_cell_index += sausage_length_rule + 1

        # Строим правый (от конца строки/колонки) вариант колбас
        current_cell_index = board_size - 1
        for sausage_index, sausage_length_rule in enumerate(
            reversed(rule_row)
        ):  # в обратном порядке берём колбаски
            sausage_end_cell = current_cell_index
            sausage_start_cell = current_cell_index - sausage_length_rule + 1

            sausages_variants_in_row[len(rule_row) - sausage_index - 1][
                "end_variant_coords"
            ] = (sausage_start_cell, sausage_end_cell)
            current_cell_index -= sausage_length_rule + 1

        sausages_variants_in_rows.append(sausages_variants_in_row)
    return sausages_variants_in_rows


def _fill_sausages_variants_intersections(
    sausages_variants_in_rows,
    board: Board,
    *,
    processing: Literal["rows", "columns"],
):
    """
    Вычисляет пересечения и «закрашивает их» по строкам или колонкам.
    """
    for row_index, row in enumerate(sausages_variants_in_rows):
        for current_sausage_variants in row.values():
            if (
                current_sausage_variants["start_variant_coords"][1]
                >= current_sausage_variants["end_variant_coords"][0]
            ):
                # Ура! Есть пересечение!
                for cell_index in range(
                    current_sausage_variants["end_variant_coords"][0],
                    current_sausage_variants["start_variant_coords"][1] + 1,
                ):
                    if processing == "rows":
                        board.fill_cell(row_index, cell_index, 1)
                    elif processing == "columns":
                        board.fill_cell(cell_index, row_index, 1)
                    else:
                        raise ValueError("incorrect processing value")


def fill_middle_parts(rules, board: Board):
    """
    Ищет середины строк и колонок, которые точно можно закрасить, и закрашивает их.
    """
    board_horizontal_size, board_vertical_size = board.get_size()

    # 1. Обходим все строки в попытке найти серединки, которые можно закрасить, и закрашиваем их
    # Надо построить самый левый вариант колбас и самый правый вариант колбас
    sausages_variants_in_rows = _find_sausages_possible_edge_variants(
        rules["horizontal"], board_horizontal_size
    )
    # Теперь надо найти пересечения одних и тех же колбасок в строках
    _fill_sausages_variants_intersections(
        sausages_variants_in_rows, board, processing="rows"
    )

    # 2. Обходим все колонки в попытке найти серединки, которые можно закрасить, и закрашиваем их
    # Надо построить самый верхний вариант колбас и самый нижний вариант колбас
    sausages_variants_in_columns = _find_sausages_possible_edge_variants(
        rules["vertical"], board_vertical_size
    )
    _fill_sausages_variants_intersections(
        sausages_variants_in_columns, board, processing="columns"
    )


def fill_empty_cells_for_partially_filled_row(rules, board: Board):
    """
    Ищет строки/колонки с одной колбаской, которая уже частично заполнена, чтобы проставить пустые ячейки
    в краях строки/колонки там, где это возможно.
    """
    board_state = board.get_state()

    # 1. Обрабатываем строки
    for row_index, row in enumerate(board_state):
        # убираем строки, в которых пока ничего не заполнено
        if not any(row):
            continue

        # убираем строки, в которых больше 1 колбаски по условиям кроссворда
        if len(rules["horizontal"][row_index]) > 1:
            continue

        # вычисляем правую сторону текущей заполненной колбасы
        right_sausage_coord = helpers.find_last_1_index(row)
        assert right_sausage_coord != -1

        if right_sausage_coord > rules["horizontal"][row_index][0]:
            # Можно слева проставить точки (пустые ячейки)
            left_dot_coord = right_sausage_coord - rules["horizontal"][row_index][0]

            for column_index in range(0, left_dot_coord + 1):
                board.fill_cell(row_index, column_index, 0)

        # вычисляем левую сторону текущей заполненной колбасы
        left_sausage_coord = helpers.find_first_1_index(row)
        assert left_sausage_coord != -1

        if left_sausage_coord + rules["horizontal"][row_index][0] < board.get_size()[0]:
            # Можно справа проставить точки (пустые ячейки)
            right_dot_coord = left_sausage_coord + rules["horizontal"][row_index][0]

            for column_index in range(right_dot_coord, board.get_size()[0]):
                board.fill_cell(row_index, column_index, 0)

    # 2. Обрабатываем столбцы
    for column_index in range(board.get_size()[0]):
        column: BoardRowState = [row[column_index] for row in board_state]

        # убираем колонки, в которых пока ничего не заполнено
        if not any(column):
            continue

        # убираем колонки, в которых больше 1 колбаски по условиям кроссворда
        if len(rules["vertical"][column_index]) > 1:
            continue

        # вычисляем верхнюю сторону текущей заполненной колбасы
        top_sausage_coord = helpers.find_first_1_index(column)
        assert top_sausage_coord != -1

        if top_sausage_coord + rules["vertical"][column_index][0] < board.get_size()[1]:
            # Можно внизу проставить точки (пустые ячейки)
            bottom_dot_coord = top_sausage_coord + rules["vertical"][column_index][0]
            for row_index in range(bottom_dot_coord, board.get_size()[1]):
                board.fill_cell(row_index, column_index, 0)

        # вычисляем нижнюю сторону текущей заполненной колбасы
        bottom_sausage_coord = helpers.find_last_1_index(column)
        assert bottom_sausage_coord != -1
        if bottom_sausage_coord > rules["vertical"][column_index][0]:
            # Можно слева проставить точки (пустые ячейки)
            left_dot_coord = bottom_sausage_coord - rules["vertical"][column_index][0]
            for row_index in range(0, left_dot_coord + 1):
                board.fill_cell(row_index, column_index, 0)


def fill_gaps_in_one_sausage(rules, board: Board):
    """
    Заполняет пробелы в единственной колбасе в строке/столбце
    """
    board_state = board.get_state()

    # 1. Обработаем строки
    for row_index, row in enumerate(board_state):
        # убираем строки, в которых пока ничего не заполнено
        if not any(row):
            continue

        # убираем строки, в которых больше 1 колбаски по условиям кроссворда
        if len(rules["horizontal"][row_index]) > 1:
            continue

        # вычисляем правую сторону текущей заполненной колбасы
        right_sausage_coord = helpers.find_last_1_index(row)
        assert right_sausage_coord != -1

        # вычисляем левую сторону текущей заполненной колбасы
        left_sausage_coord = helpers.find_first_1_index(row)
        assert left_sausage_coord != -1

        for column_index in range(left_sausage_coord + 1, right_sausage_coord):
            if board_state[row_index][column_index] == 1:
                continue
            board.fill_cell(row_index, column_index, 1)

    # 2. Обработаем столбцы
    for column_index in range(board.get_size()[0]):
        column: BoardRowState = [row[column_index] for row in board_state]

        # убираем колонки, в которых пока ничего не заполнено
        if not any(column):
            continue

        # убираем колонки, в которых больше 1 колбаски по условиям кроссворда
        if len(rules["vertical"][column_index]) > 1:
            continue

        # вычисляем верхнюю сторону текущей заполненной колбасы
        top_sausage_coord = helpers.find_first_1_index(column)
        assert top_sausage_coord != -1

        # вычисляем нижнюю сторону текущей заполненной колбасы
        bottom_sausage_coord = helpers.find_last_1_index(column)
        assert bottom_sausage_coord != -1

        for row_index in range(top_sausage_coord + 1, bottom_sausage_coord):
            if board_state[row_index][column_index] == 1:
                continue
            print("снова ура!")
            board.fill_cell(row_index, column_index, 1)


def _get_rules_file() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        sys.exit("Ошибка: не переданы входные данные")


def main():
    rules = read_crossword_rules(_get_rules_file())
    board_size = {
        "horizontal": len(rules["vertical"]),
        "vertical": len(rules["horizontal"]),
    }
    board = Board(board_size["horizontal"], board_size["vertical"])

    fill_middle_parts(rules, board)

    fill_empty_cells_for_partially_filled_row(rules, board)

    fill_gaps_in_one_sausage(rules, board)

    board.print()


if __name__ == "__main__":
    main()
