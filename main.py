import json
import logging
from pathlib import Path
from pprint import pprint


RULES_FILE = "rules.json"

logger = logging.getLogger(__name__)


def read_crossword_rules(rules_file: str):
    try:
        return json.loads(Path(rules_file).read_text())
    except:
        logger.exception("Не удалось считать правила кроссворда из файла %s", rules_file)
        raise


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
        self._board = [
            [None for _ in range(max_x) ] for _ in range(max_y)
        ]

    def get_board_size(self):
        return self._max_x, self._max_y
    
    def print(self):
        for row in self._board:
            for value in row:
                print(self.render_values[value], end="")
            print()


def fill_middle_parts(rules, board):
    """
    Ищет середины строк и колонок, которые можно закрасить
    """
    board_horizontal_size, board_vertical_size = board.get_board_size()

    # 1. Обходим все строки в попытке найти серединки, которые можно закрасить, и закрашиваем их
    # Надо построить самый левый вариант колбас и самый правый вариант колбас и найти пересечения с учётом каждой
    # колбасы в наборе колбас
    sausages_variants = []
    for row_number, rule_row in enumerate(rules["horizontal"], 1):
        sausages_variant = {sausage_index: {"left_coords": tuple(), "right_coords": tuple()} for sausage_index in range(len(rule_row))}

        # Строим левый вариант колбас
        current_cell_index = 0
        for sausage_index, sausage_length_rule in enumerate(rule_row):

            sausage_start_cell = current_cell_index
            sausage_end_cell = current_cell_index + sausage_length_rule - 1

            sausages_variant[sausage_index]["left_coords"] = (sausage_start_cell, sausage_end_cell)
            current_cell_index += sausage_length_rule + 1

        # Строим правый вариант колбас
        current_cell_index = board_horizontal_size - 1
        for sausage_index, sausage_length_rule in enumerate(reversed(rule_row)): # в обратном порядке берём колбаски
            sausage_end_cell = current_cell_index
            sausage_start_cell = current_cell_index - sausage_length_rule + 1

            sausages_variant[len(rule_row) - sausage_index - 1]["right_coords"] = (sausage_start_cell, sausage_end_cell)
            current_cell_index -= sausage_length_rule + 1

        sausages_variants.append(sausages_variant)

    for row in sausages_variants:
        print(row)
    exit()

    # 2. Обходим все колонки в попытке найти серединки, которые можно закрасить, и закрашиваем их


    


def main():
    rules = read_crossword_rules(RULES_FILE)
    #pprint(rules)
    board_size = {"horizontal": len(rules["vertical"]), "vertical": len(rules["horizontal"])}
    board = Board(board_size["horizontal"], board_size["vertical"])
    
    fill_middle_parts(rules, board)

    board.print()


if __name__ == "__main__":
    main()
