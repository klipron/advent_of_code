import os
from datetime import datetime
from collections import defaultdict

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
        top_lines, bottom_lines = list(
            map(lambda x: x.splitlines(), f.read().split("\n\n"))
        )

    stacks = defaultdict(list)
    for i, c in enumerate(top_lines[8]):
        if c.strip():
            for x in reversed(range(0, len(top_lines))):
                text = top_lines[x][i].strip()
                if text:
                    stacks[int(c)].append(text)

    moves = []
    for line in bottom_lines:
        line = line.strip()
        if not line:
            continue
        line = line.replace("move", "").replace("from", "").replace("to", "").strip()
        moves.append(tuple(map(int, line.split())))

    return stacks, moves


def part1(filename: str):
    stacks, moves = parse_file(filename)

    for x, y, z in moves:
        for _ in range(x):
            stacks[z].append(stacks[y].pop())

    return "".join(x[-1] for x in stacks.values())


def part2(filename: str):
    stacks, moves = parse_file(filename)

    for x, y, z in moves:
        stacks[z] += stacks[y][-x:]
        stacks[y] = stacks[y][:-x]

    return "".join(x[-1] for x in stacks.values())


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
