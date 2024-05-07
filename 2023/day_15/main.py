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


def calculate_hash(text: str):
    current_value = 0
    for char in text:
        current_value += ord(char[0])
        current_value *= 17
        current_value %= 256
    return current_value


def part1(path: Path):
    return sum(calculate_hash(line) for line in path.read_text().strip().split(","))


def part2(path: Path):
    boxes = {k: list() for k in range(256)}
    search_box = lambda label: next(
        (i for i, x in enumerate(boxes[box]) if x[0] == label), None
    )
    for line in path.read_text().strip().split(","):
        if "=" in line:
            label, focal_length = line.split("=")
            box = calculate_hash(label)
            lens = (label, int(focal_length))
            index = search_box(label)
            if index is None:
                boxes[box].append(lens)
            else:
                boxes[box][index] = lens
        elif line.endswith("-"):
            label = line.removesuffix("-")
            box = calculate_hash(label)
            index = search_box(label)
            if index is not None:
                boxes[box].pop(index)

    answer = 0
    for box_num, box in boxes.items():
        for slot, (_, focal_length) in enumerate(box, start=1):
            answer += (1 + box_num) * slot * focal_length
    return answer


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
