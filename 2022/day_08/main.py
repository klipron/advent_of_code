import os
from datetime import datetime

KEY_FILE = "key.txt"
INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")
TEST_FILE = os.path.join(os.path.dirname(__file__), "test.txt")


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
        data = [
            [(int(char), (x, y)) for x, char in enumerate(line.strip())]
            for y, line in enumerate(f.readlines())
        ]

    return data


def part1(filename: str):
    data = parse_file(filename)

    row_count = len(data)
    column_count = len(data[0])

    visible = set()
    for x in range(column_count):
        for row in (range(row_count), reversed(range(row_count))):
            max_height = 0
            for y in row:
                tree, pos = data[y][x]
                if (
                    (x == 0 or y == 0)
                    or (x == column_count - 1 or y == row_count - 1)
                    or tree > max_height
                ):
                    visible.add(pos)
                    max_height = tree

    for y in range(row_count):
        for column in (range(column_count), reversed(range(column_count))):
            max_height = 0
            for x in column:
                tree, pos = data[y][x]
                if (
                    (x == 0 or y == 0)
                    or (x == column_count - 1 or y == row_count - 1)
                    or tree > max_height
                ):
                    visible.add(pos)
                    max_height = tree

    return len(visible)


def part2(filename: str):
    data = parse_file(filename)

    row_count = len(data)
    column_count = len(data[0])

    scenic_scores = []
    for trees in data:
        for tree, (x, y) in trees:
            if x == 0 or y == 0 or x == column_count - 1 or y == row_count - 1:
                continue

            # top
            top_scenic_score = 0
            for i in range(1, y + 1):
                top_scenic_score += 1
                top_tree, _ = data[y - i][x]
                if top_tree >= tree:
                    break

            # bottom
            bottom_scenic_score = 0
            for i in range(y + 1, row_count):
                bottom_scenic_score += 1
                bottom_tree, _ = data[i][x]
                if bottom_tree >= tree:
                    break

            # left
            left_scenic_score = 0
            for i in range(1, x + 1):
                left_scenic_score += 1
                left_tree, _ = data[y][x - i]
                if left_tree >= tree:
                    break

            # right
            right_scenic_score = 0
            for i in range(x + 1, column_count):
                right_scenic_score += 1
                right_tree, _ = data[y][i]
                if right_tree >= tree:
                    break

            scenic_scores.append(
                top_scenic_score
                * left_scenic_score
                * bottom_scenic_score
                * right_scenic_score
            )

    return max(scenic_scores)


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
