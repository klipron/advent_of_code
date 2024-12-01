import ssl
import time
from pathlib import Path
from collections import Counter
from datetime import date, datetime
from http.client import HTTPResponse
from urllib.request import urlopen, Request

KEY_FILE = Path("key.txt")
TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


def get_input_file(advent_date: date):
    if INPUT_FILE.exists():
        return
    url = f"https://adventofcode.com/{advent_date.year}/day/{advent_date.day}/input"
    print(url)
    req = Request(url)
    req.add_header("Cookie", f"session={KEY_FILE.read_text()}")
    context = ssl._create_unverified_context()
    resp: HTTPResponse = urlopen(req, context=context)
    INPUT_FILE.write_bytes(resp.read(int(resp.getheader("Content-Length"))))


def part1(path: Path):
    lines = path.open().readlines()
    lists = zip(*(map(int, line.strip().split()) for line in lines))
    return sum(abs(int.__sub__(*x)) for x in zip(*map(sorted, lists)))


def part2(path: Path):
    lines = path.open().readlines()
    left, right = zip(*(map(int, line.strip().split()) for line in lines))
    counter = Counter(right)
    return sum(l * counter.get(l, 0) for l in left)


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    advent_date = datetime(year, 12, day)
    print(f"Advent of Code Day {advent_date.day}")
    print("=" * 80)
    if advent_date > datetime.now():
        print(
            f"Today's challenge is not ready as yet please try again in {advent_date - datetime.now()}"
        )
        return
    get_input_file(advent_date)
    file = INPUT_FILE
    print(f"Answer Part 1: {part1(file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
