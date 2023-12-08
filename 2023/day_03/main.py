import os

KEY_FILE = "key.txt"
INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def get_input_file(*, day: int, input_file: str = INPUT_FILE, key_file: str = KEY_FILE):
    with open(key_file) as f:
        key = f.read()
    os.system(
        f'curl -b "session={key}" https://adventofcode.com/2023/day/{day}/input > {input_file}'
    )


def part1(filename: str):
    with open(filename) as f:
        symb_coordinates = set()
        num_coordinates: dict[tuple[str, tuple[int, int]], list(tuple(int, int))] = {}
        num = ""
        cord = []
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line.strip()):
                if num and (x == 0 or not c.isdigit()):
                    num_coordinates[(num, cord[0])] = cord
                    num = ""
                    cord = []
                if c.isdigit():
                    num += c
                    cord.append((x, y))
                    continue
                if c == ".":
                    continue
                symb_coordinates.add((x, y))
                for a in (x, x - 1, x + 1):
                    for b in (y, y + 1, y - 1):
                        symb_coordinates.add((a, b))
    return sum(
        int(num)
        for (num, _), coord in num_coordinates.items()
        if any(x in symb_coordinates for x in coord)
    )


def part1_2(filename: str):
    total = 0
    num = ""
    cords = []
    with open(filename) as f:
        lines = [x.strip() for x in f.readlines()]
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if num and (x == 0 or not c.isdigit()):
                    adj_found = False
                    for xx, yy in cords:
                        for a in (xx, xx - 1, xx + 1):
                            if a < 0 or a >= len(line):
                                continue
                            for b in (yy, yy + 1, yy - 1):
                                if b < 0 or b >= len(lines):
                                    continue
                                ab = lines[b][a]
                                if not ab.isdigit() and ab != ".":
                                    adj_found = True
                    if adj_found:
                        total += int(num)
                    num = ""
                    cords = []
                if c.isdigit():
                    num += c
                    cords.append((x, y))
    return total


def part1_3(filename: str):
    total = 0
    num = ""
    adj_found = False
    with open(filename) as f:
        lines = [x.strip() for x in f.readlines()]
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if num and (x == 0 or not c.isdigit()):
                    if adj_found:
                        total += int(num)
                    num = ""
                    adj_found = False
                if c.isdigit():
                    num += c
                    if adj_found:
                        continue
                    for xx in (x, x - 1, x + 1):
                        if xx < 0 or xx >= len(line):
                            continue
                        for yy in (y, y + 1, y - 1):
                            if yy < 0 or yy >= len(lines):
                                continue
                            xy = lines[yy][xx]
                            if not xy.isdigit() and xy != ".":
                                adj_found = True
    return total


def part2(filename: str):
    symb_coordinates: dict[tuple[int, int], set[tuple[int, int]]] = {}
    num_coordinates: dict[tuple[str, tuple[int, int]], set[tuple[int, int]]] = {}
    num = ""
    cord = []
    with open(filename) as f:
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line.strip()):
                if num and (x == 0 or not c.isdigit()):
                    num_coordinates[(num, cord[0])] = set(cord)
                    num = ""
                    cord = []
                if c.isdigit():
                    num += c
                    cord.append((x, y))
                    continue
                if c != "*":
                    continue
                symb_coordinates[(x, y)] = set()
                for a in (x, x - 1, x + 1):
                    for b in (y, y + 1, y - 1):
                        symb_coordinates[(x, y)].add((a, b))

    gear_coords: dict[tuple[int, int], list[int]] = {}
    for symb_coord, adj_coords in symb_coordinates.items():
        gear_coords[symb_coord] = []
        for (num, _), num_coords in num_coordinates.items():
            if adj_coords.intersection(num_coords):
                gear_coords[symb_coord].append(int(num))

    return sum(v[0] * v[1] for _, v in gear_coords.items() if len(v) == 2)


def main():
    print("Advent of Code Day 3")
    input_file = INPUT_FILE
    if not os.path.exists(input_file):
        get_input_file(day=3)
        if not os.path.exists(input_file):
            return print("Failed to fetch input file.")
    print(f"Answer Part 1: {part1(input_file) or ''}")
    print(f"Answer Part 1: {part1_2(input_file) or ''}")
    print(f"Answer Part 1: {part1_3(input_file) or ''}")
    print(f"Answer Part 2: {part2(input_file) or ''}")


if __name__ == "__main__":
    main()
