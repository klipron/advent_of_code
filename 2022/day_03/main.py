import os
from string import ascii_lowercase, ascii_uppercase
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
            yield line.strip()


def calculate_priority(char: str):
    if char in ascii_uppercase:
        return ascii_uppercase.index(char) + 1 + 26
    return ascii_lowercase.index(char) + 1


def part1(filename: str):
    ans = 0
    for items in parse_file(filename):
        middle = len(items) // 2
        shared_item = (set(items[:middle]) & set(items[middle:])).pop()
        ans += calculate_priority(shared_item)

    return ans


def part2(filename: str):
    ans = 0
    lines = list(parse_file(filename))

    for i in range(0, len(lines), 3):
        shared_item = (set(lines[i]) & set(lines[i + 1]) & set(lines[i + 2])).pop()
        ans += calculate_priority(shared_item)

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
