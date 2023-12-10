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


def part1(filename: str):
    ans = 0
    data = parse_file(filename)

    choices = {"X": ("A", "C", 1), "Y": ("B", "A", 2), "Z": ("C", "B", 3)}

    for opponent_shape, player_shape in data:
        selected_shape, can_defeat_shape, choice_score = choices[player_shape]
        if opponent_shape == selected_shape:
            ans += choice_score + 3
        elif opponent_shape == can_defeat_shape:
            ans += choice_score + 6
        else:
            ans += choice_score

    return ans


def part2(filename: str):
    ans = 0
    ans = 0
    data = parse_file(filename)

    scores = {"A": 1, "B": 2, "C": 3}
    shapes = {"A": "C", "B": "A", "C": "B"}

    for opponent_shape, strategy in data:
        player_shape = None
        game_score = 0
        if strategy == "X":
            player_shape = shapes[opponent_shape]
        elif strategy == "Y":
            player_shape = opponent_shape
            game_score = 3
        else:
            player_shape = next(
                shape
                for shape, defeated_shape in shapes.items()
                if opponent_shape == defeated_shape
            )
            game_score = 6
        ans += game_score + scores[player_shape]
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
