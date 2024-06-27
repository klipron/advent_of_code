import re
from pathlib import Path
from datetime import date
from typing import Iterable
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


def move(char: str, point: tuple[int, int], amount: int = 1):
    x, y = point
    if char in ("U", "3"):
        return (x, y - amount)
    elif char in ("D", "1"):
        return (x, y + amount)
    elif char in ("L", "2"):
        return (x - amount, y)
    elif char in ("R", "0"):
        return (x + amount, y)
    else:
        raise ValueError(f"Invalid character {char}.")


def calculate_area(polygon: Iterable[tuple[str, int]]):
    area = 0
    total_length = 0
    current_point = (0, 0)
    for direction, side_length in polygon:
        next_point = move(direction, current_point, side_length)
        x, y = current_point
        x1, y1 = next_point
        area += ((x * y1) - (x1 * y)) / 2
        total_length += side_length
        current_point = next_point
    return total_length + (int(abs(area)) - (total_length // 2)) + 1


def part1(path: Path):
    polygon = []
    for line in path.open().readlines():
        char, num, _ = line.split()
        polygon.append((char, int(num)))
    return calculate_area(polygon)


def part2(path: Path):
    polygon = []
    for line in path.open().readlines():
        # text = re.search(r"\(#(?P<value>\w+)\)", line).group("value")
        text = re.sub(r"[\(\)#]", "", line.split()[-1])
        char = text[-1]
        num = int(text[:-1], base=16)
        polygon.append((char, num))
    return calculate_area(polygon)


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
    file = TEST_FILE
    print(f"Answer Part 1: {part1(file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
