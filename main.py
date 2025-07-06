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


def init_board(max_x: int, max_y: int):
    # координаты верхнего левого угла: (0, 0)
    # координаты правого нижнего угла: (max_x - 1, max_y - 1)
    return [
        [None for column in range(max_x) ] for row in range(max_y)
    ]


def print_board(board):
    render_values = {
        None: "\033[90m?\033[90m ",  # неизвестно
        1: "\033[32m♥\033[00m ",  # закрашено
        0: "\033[32m‧\033[00m ",  # не закрашено
    }
    for row in board:
        for value in row:
            print(render_values[value], end="")
        print()



def main():
    rules = read_crossword_rules(RULES_FILE)
    #pprint(rules)
    field = {"horizontal": len(rules["vertical"]), "vertical": len(rules["horizontal"])}
    board = init_board(field["horizontal"], field["vertical"])
    print_board(board)


if __name__ == "__main__":
    main()
