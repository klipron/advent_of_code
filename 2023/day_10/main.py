import os
from enum import Enum
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
    data = {}
    with open(filename) as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            if not line:
                continue
            for x, char in enumerate(line):
                data[(x, y)] = char
    return data


class Direction(Enum):
    N = 1
    S = 2
    W = 3
    E = 4


def move(pos: tuple[int, int], direction: Direction):
    x, y = pos
    if direction == Direction.N:
        return (x, y - 1)
    if direction == Direction.S:
        return (x, y + 1)
    if direction == Direction.W:
        return (x - 1, y)
    if direction == Direction.E:
        return (x + 1, y)


def move_through_pipe(pipe: str, direction: Direction):
    if pipe == "|":
        if direction not in (Direction.N, Direction.S):
            return
        return direction
    if pipe == "-":
        if direction not in (Direction.W, Direction.E):
            return
        return direction
    if pipe == "L":
        if direction not in (Direction.S, Direction.W):
            return
        if direction == Direction.S:
            return Direction.E
        return Direction.N
    if pipe == "J":
        if direction not in (Direction.S, Direction.E):
            return
        if direction == Direction.S:
            return Direction.W
        return Direction.N
    if pipe == "7":
        if direction not in (Direction.N, Direction.E):
            return
        if direction == Direction.N:
            return Direction.W
        return Direction.S
    if pipe == "F":
        if direction not in (Direction.N, Direction.W):
            return
        if direction == Direction.N:
            return Direction.E
        return Direction.S


def get_loop_postions(grid: dict[tuple[int, int], str]):
    start_pos = next(pos for pos, char in grid.items() if char == "S")
    yield start_pos

    max_width = max(x for x, _ in grid.keys())
    max_length = max(y for _, y in grid.keys())

    for direction in Direction.E, Direction.N, Direction.S, Direction.W:
        pos = move(start_pos, direction)
        x, y = pos
        if x < 0 or y < 0 or x >= max_width or y >= max_length:
            continue
        direction = move_through_pipe(grid[pos], direction)
        if direction is not None:
            yield pos
            break

    while grid[pos] != "S":
        pos = move(pos, direction)
        yield pos
        direction = move_through_pipe(grid[pos], direction)


def part1(filename: str):
    data = parse_file(filename)
    ans = len(list(get_loop_postions(data))) // 2

    return ans


def part2(filename: str):
    data = parse_file(filename)
    loop_positions = list(get_loop_postions(data))

    area = 0
    for i in range(len(loop_positions) - 1):
        x, y = loop_positions[i]
        x1, y1 = loop_positions[i + 1]
        area += ((x * y1) - (x1 * y)) / 2

    ans = int(abs(area)) - (len(loop_positions) // 2) + 1
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
