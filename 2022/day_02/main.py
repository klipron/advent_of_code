import os
from datetime import datetime

KEY_FILE = "key.txt"
INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def get_input_file(
    *, advent_date: datetime, input_file: str = INPUT_FILE, key_file: str = KEY_FILE
):
    with open(key_file) as f:
        key = f.read()
    os.system(
        f'curl -b "session={key}" https://adventofcode.com/{advent_date.year}/day/{advent_date.day}/input > {input_file}'
    )


def parse_file(filename: str):
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            yield tuple(line.split())


SCORES = {"A": 1, "B": 2, "C": 3}
DEFEATED_SHAPES = {"A": "C", "B": "A", "C": "B"}
STRATEGY_SHAPES = {"X": "A", "Y": "B", "Z": "C"}


def part1(filename: str):
    ans = 0

    for opponent_shape, player_shape in parse_file(filename):
        selected_shape = STRATEGY_SHAPES[player_shape]
        player_score = SCORES[selected_shape]
        ans += player_score
        ans += (
            3
            if opponent_shape == selected_shape
            else 6
            if opponent_shape == DEFEATED_SHAPES[selected_shape]
            else 0
        )

    return ans


def part2(filename: str):
    ans = 0

    for opponent_shape, strategy in parse_file(filename):
        if strategy == "X":
            ans += SCORES[DEFEATED_SHAPES[opponent_shape]]
        elif strategy == "Y":
            ans += SCORES[opponent_shape] + 3
        else:
            ans += SCORES[
                next(
                    shape
                    for shape, defeated_shape in DEFEATED_SHAPES.items()
                    if opponent_shape == defeated_shape
                )
            ]
            ans += 6
    return ans


def main():
    day = int(os.path.split(os.path.dirname(__file__))[1].split("_")[1])
    year = os.path.split(os.path.split(os.path.dirname(__file__))[0])[1]
    advent_date = datetime(int(year), 12, day)
    print(f"Advent of Code Day {advent_date.day}")
    print("=" * 80)
    if advent_date > datetime.now():
        print(
            f"Today's challenge is not ready as yet please try again in {advent_date - datetime.now()}"
        )
        return
    input_file = INPUT_FILE
    if not os.path.exists(input_file):
        get_input_file(advent_date=advent_date)
        if not os.path.exists(input_file):
            return print("Failed to fetch input file.")
    print(f"Answer Part 1: {part1(input_file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(input_file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
