import re
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


def move(char: str, point: tuple[int, int]):
    x, y = point
    if char in ("U", "3"):
        return (x, y - 1)
    elif char in ("D", "1"):
        return (x, y + 1)
    elif char in ("L", "2"):
        return (x - 1, y)
    elif char in ("R", "0"):
        return (x + 1, y)
    else:
        raise ValueError(f"Invalid character {char}.")


def part1(path: Path):
    area = 0
    length = 1
    current_point = (0, 0)
    for line in path.open().readlines():
        char, num, _ = line.split(maxsplit=2)
        for _ in range(int(num)):
            next_point = move(char, current_point)
            x, y = current_point
            x1, y1 = next_point
            area += ((x * y1) - (x1 * y)) / 2
            length += 1
            current_point = next_point
    return length + int(abs(area)) - (length // 2)


def part2(path: Path):
    area = 0
    length = 1
    current_point = (0, 0)
    lines = path.open().readlines()
    total_lines = len(lines)
    for i, line in enumerate(lines, start=1):
        text = re.search(r"\(#(?P<value>\w+)\)", line).group("value")
        char = text[-1]
        num = text[:-1]
        for _ in range(int(num, base=16)):
            next_point = move(char, current_point)
            x, y = current_point
            x1, y1 = next_point
            area += ((x * y1) - (x1 * y)) / 2
            length += 1
            current_point = next_point
        print(f"{i} of {total_lines}", end="\r")
    return length + int(abs(area)) - (length // 2)


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
    file = INPUT_FILE
    print(f"Answer Part 1: {part1(file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
