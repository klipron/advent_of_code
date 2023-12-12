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
        for i, line in enumerate(f.readlines()):
            yield [c for c in line.strip()]


def expand_universe(data: list[list[str]], *, expansion=1):
    expanded_universe: list[list[str]] = []
    for line in data:
        if "#" in line:
            expanded_universe.append(line)
            continue
        expanded_universe.append(line)
        for _ in range(expansion - (0 if expansion == 1 else 1)):
            expanded_universe.append([x.replace(".", "@") for x in line])

    x = 0
    while x < len(expanded_universe[0]):
        if any(expanded_universe[y][x] == "#" for y in range(len(expanded_universe))):
            x += 1
            continue
        for y in range(len(expanded_universe)):
            for _ in range(expansion - (0 if expansion == 1 else 1)):
                expanded_universe[y].insert(x + 1, "@")
        x += 2

    return expanded_universe


def expand_older_universe(data: list[list[str]], *, expansion: int = 1):
    universe: dict[tuple[int, int], str] = {}

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            universe[(x, y)] = char

    max_width = max(x for x, _ in universe.keys())
    max_length = max(y for _, y in universe.keys())

    expanded_universe: dict[tuple[int, int], tuple[int, int]] = {
        k: k for k, _ in universe.items()
    }

    for i in range(max_width):
        if all(c == "." for (a, _), c in universe.items() if a == i):
            for k, (x, y) in expanded_universe.items():
                if k[0] > i:
                    expanded_universe[k] = (
                        x - (0 if expansion == 1 else 1) + expansion,
                        y,
                    )

    for i in range(max_length):
        if all(c == "." for (_, b), c in universe.items() if b == i):
            for k, (x, y) in expanded_universe.items():
                if k[1] > i:
                    expanded_universe[k] = (
                        x,
                        y - (0 if expansion == 1 else 1) + expansion,
                    )

    return {v: universe[k] for k, v in expanded_universe.items()}


def calculate_shortest_paths(galaxies: list[tuple[int, int]]):
    galaxy_pairs: dict[tuple[tuple[int, int], tuple[int, int]]] = dict()
    for galaxy1 in sorted(galaxies):
        for galaxy2 in sorted(galaxies):
            if galaxy1 == galaxy2:
                continue
            galaxy_pairs[tuple(sorted((galaxy1, galaxy2)))] = 0

    for pair in galaxy_pairs:
        (x1, y1), (x2, y2) = pair
        galaxy_pairs[pair] = (max(x1, x2) - min(x1, x2)) + (max(y1, y2) - min(y1, y2))

    return galaxy_pairs


def part1(filename: str):
    data = list(parse_file(filename))
    expanded_universe = expand_universe(data, expansion=1)

    galaxies = []
    for y, line in enumerate(expanded_universe):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append((x, y))

    shortest_paths = calculate_shortest_paths(galaxies)
    return sum(shortest_paths.values())


def part2(filename: str):
    data = list(parse_file(filename))
    expanded_universe = expand_older_universe(data, expansion=1_000_000)
    galaxies = [k for k, v in expanded_universe.items() if v == "#"]
    shortest_paths = calculate_shortest_paths(galaxies)
    return sum(shortest_paths.values())


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
