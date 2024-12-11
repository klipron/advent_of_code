import time

start = time.time()

import os
import ssl
from pathlib import Path
from collections import Counter
from functools import lru_cache
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


def solve(path: Path, test=False):
    counter = Counter(map(int, path.read_text().strip().split()))
    changes: dict[int, list[int]] = {0: (1,)}
    for i in range(75):
        new_counter = Counter()
        for num in counter:
            if num not in changes:
                text = str(num)
                idx, rem = divmod(len(text), 2)
                changes[num] = (
                    (int(text[:idx]), int(text[idx:])) if rem == 0 else (num * 2024,)
                )
            for _num in changes[num]:
                new_counter.update({_num: counter[num]})
        counter = new_counter.copy()
        if i + 1 == 25:
            show_answer(part=1, answer=counter.total(), test=test)

    show_answer(part=2, answer=counter.total(), test=test)


def get_input_file(year: int, day: int):
    if INPUT_FILE.exists():
        return
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    req = Request(url)
    req.add_header("Cookie", f"session={os.environ["AOC_SESSION"]}")
    context = ssl._create_unverified_context()
    try:
        resp: HTTPResponse = urlopen(req, context=context)
    except HTTPError as e:
        return print(e.read().decode())
    INPUT_FILE.write_bytes(resp.read(int(resp.getheader("Content-Length"))))


def show_answer(*, part: int, answer: int, test=False):
    print(
        f"{"Test Input " if test else ""}Answer Part {part}: {answer or ''}".ljust(50),
        "=" * 80,
        sep="\n",
    )


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    print(f"Advent of Code {year} Day {day}")
    print("=" * 80)
    get_input_file(year, day)
    if not INPUT_FILE.exists():
        return
    if TEST_FILE.exists():
        solve(TEST_FILE, test=True)
    solve(INPUT_FILE)


if __name__ == "__main__":
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
