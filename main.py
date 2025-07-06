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
    for row_number, row in enumerate(rules["horizontal"], 1):
        empty_row = [0 for _ in range(board_horizontal_size)]

        # 2, 8, 3 — in filled_cells_rule

        # построить самый левый вариант колбас и самый правый вариант колбас и найти пересечения с учётом каждой
        # колбасы в наборе колбас

        # строим левый вариант колбас
        current_cell_index = 0
        for sausage_length_rule in row:
            for index in range(sausage_length_rule):
                empty_row[index + current_cell_index] = 1
            current_cell_index += sausage_length_rule + 1
        print(row_number, empty_row)
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
