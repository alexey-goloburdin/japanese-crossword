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


def main():
    rules = read_crossword_rules(RULES_FILE)
    pprint(rules)
    field = {"horizontal": len(rules["vertical"]), "vertical": len(rules["horizontal"])}


if __name__ == "__main__":
    main()
