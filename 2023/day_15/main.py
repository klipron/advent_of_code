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
    boxes = [list() for _ in range(256)]
    search_box = lambda label, box: next(
        (i for i, (lens_label, _) in enumerate(box) if lens_label == label), None
    )
    for line in path.read_text().strip().split(","):
        if "=" in line:
            label, focal_length = line.split("=")
            box_idx = calculate_hash(label)
            lens = (label, int(focal_length))
            lens_idx = search_box(label, boxes[box_idx])
            if lens_idx is None:
                boxes[box_idx].append(lens)
            else:
                boxes[box_idx][lens_idx] = lens
        elif line.endswith("-"):
            label = line.removesuffix("-")
            box_idx = calculate_hash(label)
            lens_idx = search_box(label, boxes[box_idx])
            if lens_idx is not None:
                boxes[box_idx].pop(lens_idx)

    answer = 0
    for box_num, box_idx in enumerate(boxes, start=1):
        for slot, (_, focal_length) in enumerate(box_idx, start=1):
            answer += box_num * slot * focal_length
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
