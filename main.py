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
    # 1. Обходим все строки в попытке найти серединки, которые можно закрасить, и закрашиваем их
    board_horizontal_size, board_vertical_size = board.get_board_size()
    for row_number, row in enumerate(rules["horizontal"], 1):
        if sum(row) > board_horizontal_size / 2:
            print(f"в строке № {row_number} можно чёт закрасить, строка: {row}")

    # 2. Обходим все колонки в попытке найти серединки, которые можно закрасить, и закрашиваем их

def main():
    rules = read_crossword_rules(RULES_FILE)
    #pprint(rules)
    board_size = {"horizontal": len(rules["vertical"]), "vertical": len(rules["horizontal"])}
    board = Board(board_size["horizontal"], board_size["vertical"])
    
    fill_middle_parts(rules, board)

    #board.print()


if __name__ == "__main__":
    main()
