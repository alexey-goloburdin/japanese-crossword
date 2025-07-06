import json
import logging
from pathlib import Path
from pprint import pprint
from typing import Literal


RULES_FILE = "rules.json"

logger = logging.getLogger(__name__)


def read_crossword_rules(rules_file: str):
    try:
        return json.loads(Path(rules_file).read_text())
    except:
        logger.exception("Не удалось считать правила кроссворда из файла %s", rules_file)
        raise


class IncorrectCellFill(Exception):
    """Неудачная попытка перевести статус клеточки в 0 или 1"""


class Board:
    """
    Координаты верхнего левого угла: (0, 0)
    Координаты правого нижнего угла: (max_x - 1, max_y - 1)
    """
    render_values = {
        None: "\033[90m?\033[90m ",  # неизвестно
        1: "\033[32m♥\033[00m ",  # закрашено
        0: "\033[32m‧\033[00m ",  # не закрашено
    }

    def __init__(self, max_x: int, max_y: int):
        self._max_x = max_x
        self._max_y = max_y
        # В self._board храним массив строк
        self._board: list[list[Literal[0] | Literal[1] | None]] = [
            [None for _ in range(max_x) ] for _ in range(max_y)
        ]

    def get_board_size(self):
        return self._max_x, self._max_y

    def fill_cell(self, row: int, column: int, value: Literal[0] | Literal[1]):
        old_cell_value = self._board[row][column]
        if old_cell_value is not None and old_cell_value != value:
            raise IncorrectCellFill(f"Статус ячейки ({row}, {column}) был {old_cell_value}, нельзя перевести в {value}")
        self._board[row][column] = value
    
    def print(self):
        self._print_column_numbers_header()
        for row_number, row in enumerate(self._board, 1):
            self._print_row_header(row_number)
            for value in row:
                print(self.render_values[value], end="")
            print()

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


def fill_middle_parts(rules, board):
    """
    Ищет середины строк и колонок, которые можно закрасить
    """
    board_horizontal_size, board_vertical_size = board.get_board_size()

    # 1. Обходим все строки в попытке найти серединки, которые можно закрасить, и закрашиваем их
    # Надо построить самый левый вариант колбас и самый правый вариант колбас
    sausages_variants_in_rows = []  # список строк с гипотетическими вариантами колбасок
    for rule_row in rules["horizontal"]:
        # гипотетические положения колбасок в текущей строке
        sausages_variants_in_row = {sausage_index: {"left_variant_coords": tuple(),
                                                    "right_variant_coords": tuple()}
                                    for sausage_index in range(len(rule_row))}

        # Строим левый вариант колбас
        current_cell_index = 0
        for sausage_index, sausage_length_rule in enumerate(rule_row):
            sausage_start_cell = current_cell_index
            sausage_end_cell = current_cell_index + sausage_length_rule - 1

            sausages_variants_in_row[sausage_index]["left_variant_coords"] = (sausage_start_cell, sausage_end_cell)
            current_cell_index += sausage_length_rule + 1

        # Строим правый вариант колбас
        current_cell_index = board_horizontal_size - 1
        for sausage_index, sausage_length_rule in enumerate(reversed(rule_row)): # в обратном порядке берём колбаски
            sausage_end_cell = current_cell_index
            sausage_start_cell = current_cell_index - sausage_length_rule + 1

            sausages_variants_in_row[len(rule_row) - sausage_index - 1]["right_variant_coords"] = (sausage_start_cell, sausage_end_cell)
            current_cell_index -= sausage_length_rule + 1

        sausages_variants_in_rows.append(sausages_variants_in_row)

    # for row in sausages_variants_in_rows:
    #     print(row)

    # Теперь надо найти пересечения одних и тех же колбасок в строках
    for row_index, row in enumerate(sausages_variants_in_rows):
        for sausage_index, current_sausage_variants in row.items():
            if current_sausage_variants["left_variant_coords"][1] >= current_sausage_variants["right_variant_coords"][0]:
                # Ура! Есть пересечение!
                for cell_index in range(current_sausage_variants["right_variant_coords"][0],
                                        current_sausage_variants["left_variant_coords"][1] + 1):
                    board.fill_cell(row_index, cell_index, 1)

    # 2. Обходим все колонки в попытке найти серединки, которые можно закрасить, и закрашиваем их
    # Надо построить самый верхний вариант колбас и самый нижний вариант колбас
    sausages_variants_in_columns = []  # список колонок с гипотетическими вариантами колбасок
    for rule_column in rules["vertical"]:
        # гипотетические положения колбасок в текущей колонке
        sausages_variants_in_column = {sausage_index: {"top_variant_coords": tuple(),
                                                       "bottom_variant_coords": tuple()}
                                       for sausage_index in range(len(rule_column))}

        # Строим верхний вариант колбас
        current_cell_index = 0
        for sausage_index, sausage_length_rule in enumerate(rule_column):
            sausage_start_cell = current_cell_index
            sausage_end_cell = current_cell_index + sausage_length_rule - 1

            sausages_variants_in_column[sausage_index]["top_variant_coords"] = (sausage_start_cell, sausage_end_cell)
            current_cell_index += sausage_length_rule + 1

        # Строим нижний вариант колбас
        current_cell_index = board_vertical_size - 1
        for sausage_index, sausage_length_rule in enumerate(reversed(rule_column)): # в обратном порядке берём колбаски
            sausage_end_cell = current_cell_index
            sausage_start_cell = current_cell_index - sausage_length_rule + 1

            sausages_variants_in_column[len(rule_column) - sausage_index - 1]["bottom_variant_coords"] = (sausage_start_cell, sausage_end_cell)
            current_cell_index -= sausage_length_rule + 1

        sausages_variants_in_columns.append(sausages_variants_in_column)

    # for row in sausages_variants_in_columns:
    #     print(row)

    # Теперь надо найти пересечения одних и тех же колбасок в колонках
    for column_index, column in enumerate(sausages_variants_in_columns):
        for sausage_index, current_sausage_variants in column.items():
            if current_sausage_variants["top_variant_coords"][1] >= current_sausage_variants["bottom_variant_coords"][0]:
                # Ура! Есть пересечение!
                for cell_index in range(current_sausage_variants["bottom_variant_coords"][0],
                                        current_sausage_variants["top_variant_coords"][1] + 1):
                    board.fill_cell(cell_index, column_index, 1)


def main():
    rules = read_crossword_rules(RULES_FILE)
    board_size = {"horizontal": len(rules["vertical"]), "vertical": len(rules["horizontal"])}
    board = Board(board_size["horizontal"], board_size["vertical"])
    
    fill_middle_parts(rules, board)

    board.print()


if __name__ == "__main__":
    main()
