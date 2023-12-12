import os
from datetime import datetime
from collections import defaultdict

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
        for _ in range(expansion):
            expanded_universe.append([x.replace(".", "@") for x in line])

    # for line in expanded_universe:
    #     print(line)
    print("=" * 80)
    # return

    # line = expanded_universe[0]
    # print(expanded_universe[0])
    offset = 0
    x = 0
    while x < len(expanded_universe[0]):
        # if x > 20:
        #     break
        # print(f"{x=}")
        if any(expanded_universe[y][x] == "#" for y in range(len(expanded_universe))):
            x += 1
            continue
        # print(x)
        for y in range(len(expanded_universe)):
            # expanded_universe[y] = (
            #     expanded_universe[y][: x + offset]
            #     + "."
            #     + expanded_universe[y][x + offset :]
            # )
            # print(expanded_universe[y])
            # print(f"{(x,y)=}")
            for _ in range(expansion):
                expanded_universe[y].insert(x + 1, "@")
            # for line in expanded_universe:
            #     print(line)
            # print("=" * 80)
        x += 2
        # print(f"{len(expanded_universe[0])=}")
        # print(f"{offset=}")

    # for line in expanded_universe:
    #     print(line)
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
            print(f"{i=}")
            # print({k: v for k, v in universe.items() if k[0] == i})
            for k, (x, y) in expanded_universe.items():
                if k[0] > i:
                    if k[0] == 8:
                        print(k, x + expansion - 1, y)
                    expanded_universe[k] = x + expansion - 1, y

    for i in range(max_length):
        if all(c == "." for (_, b), c in universe.items() if b == i):
            for k, (x, y) in expanded_universe.items():
                if k[1] > i:
                    expanded_universe[k] = x, y + expansion - 1

    return {v: universe[k] for k, v in expanded_universe.items()}


def part1(filename: str):
    data = list(parse_file(filename))
    expanded_universe = expand_universe(data, expansion=1)
    print(f"{len(expanded_universe)=}")

    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as f:
        for x in expanded_universe:
            f.write("".join(x))
            f.write("\n")

    # return

    galaxies = []
    for y, line in enumerate(expanded_universe):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append((x, y))

    print(f"{len(galaxies)=}")

    galaxy_pairs: dict[tuple[tuple[int, int], tuple[int, int]]] = dict()
    for galaxy1 in sorted(galaxies):
        for galaxy2 in sorted(galaxies):
            if galaxy1 == galaxy2:
                continue
            galaxy_pairs[tuple(sorted((galaxy1, galaxy2)))] = 0

    for i, pair in enumerate(galaxy_pairs):
        # if i < 10:
        #     print(pair)
        (x1, y1), (x2, y2) = pair
        galaxy_pairs[pair] = (max(x1, x2) - min(x1, x2)) + (max(y1, y2) - min(y1, y2))

    print(f"{len(galaxy_pairs)=}")
    # for k, v in galaxy_pairs.items():
    #     (x, y), (a, b) = k
    # if (x, y) != (0, 11):
    #     continue
    # print(k, v)

    return sum(galaxy_pairs.values())


def part2(filename: str):
    data = list(parse_file(filename))
    expanded_universe = expand_older_universe(data, expansion=1_000_000)
    print(f"{len(expanded_universe)=}")

    # with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as f:
    #     for x in expanded_universe:
    #         f.write("".join(x))
    #         f.write("\n")

    # return

    galaxies = [k for k, v in expanded_universe.items() if v == "#"]
    print(f"{len(galaxies)=}")

    galaxy_pairs: dict[tuple[tuple[int, int], tuple[int, int]]] = dict()
    for galaxy1 in sorted(galaxies):
        for galaxy2 in sorted(galaxies):
            if galaxy1 == galaxy2:
                continue
            galaxy_pairs[tuple(sorted((galaxy1, galaxy2)))] = 0

    for i, pair in enumerate(galaxy_pairs):
        # if i < 10:
        #     print(pair)
        (x1, y1), (x2, y2) = pair
        galaxy_pairs[pair] = (max(x1, x2) - min(x1, x2)) + (max(y1, y2) - min(y1, y2))

    print(f"{len(galaxy_pairs)=}")
    # for k, v in galaxy_pairs.items():
    #     (x, y), (a, b) = k
    # if (x, y) != (0, 11):
    #     continue
    # print(k, v)

    return sum(galaxy_pairs.values())


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
