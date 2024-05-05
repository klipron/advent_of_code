from pathlib import Path
from datetime import date
from collections import defaultdict
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


def iter_patterns(path: Path):
    pattern: list[str] = []
    with path.open() as f:
        while line := f.readline():
            if line == "\n":
                yield pattern.copy()
                pattern = []
                continue
            pattern.append(line.strip())
    if pattern:
        yield pattern


def as_columns(rows: list[str]):
    columns: list[str] = []
    for row in rows:
        if not columns:
            columns = ["" for _ in row]
        for i, c in enumerate(row):
            columns[i] += c
    return columns


def is_mirrored(lines: list[str]):
    if len(lines) % 2 != 0:
        return False
    mid = len(lines) // 2
    return tuple(lines[:mid]) == tuple(reversed(lines[mid:]))


def iter_mirror_edges(lines: list[str]):
    last_idx = len(lines) - 1
    line_indexes = defaultdict(list[int])
    for i, line in enumerate(lines):
        if i in (0, last_idx):
            continue
        line_indexes[line].append(i)

    indexes = line_indexes.get(lines[0])
    if indexes is not None:
        for index in sorted(indexes, reverse=True):
            if is_mirrored(lines[: index + 1]):
                yield int(), index
    indexes = line_indexes.get(lines[-1])
    if indexes is not None:
        for index in indexes:
            if is_mirrored(lines[index:]):
                yield index, last_idx


def summarize_pattern(top: int, bottom: int, *, is_row: bool):
    return (top + ((bottom - top + 1) // 2)) * (100 if is_row else 1)


def part1(path: Path):
    answer = 0
    for pattern in iter_patterns(path):
        for i, lines in enumerate((pattern, as_columns(pattern))):
            edges = next(iter_mirror_edges(lines), None)
            top, bottom = edges if edges is not None else (0, 0)
            answer += summarize_pattern(top, bottom, is_row=i == 0)
    return answer


def pattern_to_nums(pattern: list[str]):
    return [int(line.replace(".", "0").replace("#", "1"), base=2) for line in pattern]


def get_alternate_patterns(pattern: list[str]):
    nums = pattern_to_nums(pattern)
    for ix, x in enumerate(nums):
        for iy, y in enumerate(nums):
            if ix == iy or ix > iy:
                continue
            if bin(x ^ y).count("1") == 1:
                new_pattern = [
                    pattern[ix] if i == iy else z for i, z in enumerate(pattern)
                ]
                if is_mirrored(new_pattern[ix : iy + 1]):
                    yield new_pattern, (ix, iy)


def part2(path: Path):
    answer = 0
    for pattern in iter_patterns(path):
        for i, lines in enumerate((pattern, as_columns(pattern))):
            for new_pattern, changes in get_alternate_patterns(lines):
                if new_pattern is None:
                    continue
                for edges in iter_mirror_edges(new_pattern):
                    if edges is None:
                        continue
                    top, bottom = edges
                    if not all(x in range(top, bottom + 1) for x in changes):
                        continue
                    answer += summarize_pattern(top, bottom, is_row=i == 0)
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
    file = INPUT_FILE
    print(f"Answer Part 1: {part1(file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
