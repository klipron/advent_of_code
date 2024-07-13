import time
from pathlib import Path
from datetime import date
from http.client import HTTPResponse
from urllib.request import urlopen, Request

KEY_FILE = Path("key.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")
TEST_FILE = Path(__file__).with_name("test.txt")


def get_input_file(advent_date: date):
    if INPUT_FILE.exists():
        return
    url = f"https://adventofcode.com/{advent_date.year}/day/{advent_date.day}/input"
    req = Request(url)
    req.add_header("Cookie", f"session={KEY_FILE.read_text()}")
    resp: HTTPResponse = urlopen(req)
    INPUT_FILE.write_bytes(resp.read(int(resp.getheader("Content-Length"))))


def get_grid(path: Path):
    grid = {}
    for y, line in enumerate(path.open().readlines()):
        for x, char in enumerate(line.strip()):
            grid[(x, y)] = char
    return grid


def move(pos: tuple[int, int]):
    x, y = pos
    yield (x, y - 1)
    yield (x, y + 1)
    yield (x + 1, y)
    yield (x - 1, y)


def part1(path: Path, steps: int):
    grid = get_grid(path)
    rock_pos = set(k for k, v in grid.items() if v == "#")
    possible_steps = {
        k: tuple(x for x in move(k) if x not in rock_pos)
        for k, v in grid.items()
        if v != "#"
    }
    tiles = set(k for k, v in grid.items() if v == "S")
    next_tiles = set()
    for _ in range(steps):
        next_tiles = set()
        while tiles:
            pos = tiles.pop()
            for tile in possible_steps[pos]:
                next_tiles.add(tile)
        tiles = next_tiles.copy()
    return len(next_tiles)


def part2(path: Path, steps: int):
    grid = get_grid(path)
    width = sum(1 for x, _ in grid.keys() if x == 0)
    length = sum(1 for _, y in grid.keys() if y == 0)

    rock_pos = set(k for k, v in grid.items() if v == "#")
    possible_steps = {
        k: tuple(x for x in move(k) if x not in rock_pos)
        for k, v in grid.items()
        if v != "#"
    }
    offset_mapping: dict[tuple[int, int], list[tuple[int, int]]] = {}

    def outer_possible_steps(pos: tuple[int, int]):
        if pos in possible_steps:
            for next_steps in possible_steps[pos]:
                yield next_steps
            return
        if pos in offset_mapping:
            for next_steps in offset_mapping[pos]:
                yield next_steps
            return
        x, y = pos
        x_offset = 0
        if x < 0 or x > width - 1:
            x_offset = (
                (((abs(x) - 1 if x < 0 else x - width) // width) + 1) * width
            ) * (1 if x < 0 else -1)
        y_offset = 0
        if y < 0 or y > length - 1:
            y_offset = (
                (((abs(y) - 1 if y < 0 else y - length) // length) + 1) * length
            ) * (1 if y < 0 else -1)

        offset_mapping[pos] = []
        for _x, _y in possible_steps[(x + x_offset, y + y_offset)]:
            yield (_x - x_offset, _y - y_offset)
            offset_mapping[pos].append((_x - x_offset, _y - y_offset))

    diffs = []
    values = []
    tiles = set(k for k, v in grid.items() if v == "S")
    next_tiles = set()
    curr = 0
    prev = 0
    step_count = 0
    while True:
        step_count += 1
        if step_count > steps:
            return curr
        next_tiles = set()
        while tiles:
            pos = tiles.pop()
            for tile in outer_possible_steps(pos):
                next_tiles.add(tile)
        tiles = next_tiles.copy()
        curr = len(next_tiles)
        diff = curr - prev
        prev = curr
        diffs.append(diff)
        diffs = diffs[(width * 2) * -1 :]
        values.append(diff - diffs[(width + 1) * -1 :][0])
        values = values[(width * 2) * -1 :]
        if (
            len(values) == width * 2
            and values[: (len(values) // 2)] == values[len(values) // 2 :]
        ):
            break

    idx = (len(values) // 2) * -1
    values = values[idx:]
    diffs = diffs[idx:]
    while True:
        diffs = tuple(a + b for a, b in zip(values, diffs))
        for val in diffs:
            step_count += 1
            if step_count > steps:
                break
            curr += val
        else:
            continue
        break
    return curr


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    advent_date = date(year, 12, day)
    print(f"Advent of Code Day {advent_date.day}")
    print("=" * 80)
    if advent_date > date.today():
        print(
            f"Today's challenge is not ready as yet please try again in {advent_date - date.today()}"
        )
        return
    get_input_file(advent_date)
    for file, part_1, part_2 in ((TEST_FILE, 6, 5000), (INPUT_FILE, 64, 26501365)):
        print(f"Answer Part 1: {part1(file, part_1) or ''}")
        print("=" * 80)
        print(f"Answer Part 2: {part2(file, part_2) or ''}")
        print("=" * 80)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start} seconds."
    )
