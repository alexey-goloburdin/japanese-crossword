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
        self._board = [
            [None for _ in range(max_x) ] for _ in range(max_y)
        ]

    def print(self):
        for row in self._board:
            for value in row:
                print(self.render_values[value], end="")
            print()



def main():
    rules = read_crossword_rules(RULES_FILE)
    #pprint(rules)
    board_size = {"horizontal": len(rules["vertical"]), "vertical": len(rules["horizontal"])}
    board = Board(board_size["horizontal"], board_size["vertical"])
    board.print()


if __name__ == "__main__":
    main()
