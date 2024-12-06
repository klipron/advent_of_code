import os
import ssl
import time
from pathlib import Path
from typing import Callable, Any
from functools import cmp_to_key
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


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


def solve(path: Path, show_answer: Callable[[int, Any], None]):
    top, bottom = path.read_text().split("\n\n")
    ordering_rules = set(tuple(map(int, z.split("|"))) for z in top.split())
    pages_to_produce = tuple(tuple(map(int, z.split(","))) for z in bottom.split())

    part1 = 0
    part2 = 0
    for pages in pages_to_produce:
        for i, page in enumerate(pages):
            for next_page in pages[i + 1 :]:
                if (page, next_page) not in ordering_rules:
                    break
            else:
                continue
            break
        else:
            part1 += pages[len(pages) // 2]
            continue
        ordered_pages = []
        for page in pages:
            for i, ordered_page in enumerate(ordered_pages):
                if (page, ordered_page) in ordering_rules:
                    ordered_pages.insert(i, page)
                    break
            else:
                ordered_pages.append(page)
        part2 += ordered_pages[len(ordered_pages) // 2]

    show_answer(1, part1)
    show_answer(2, part2)


def solve_v2(path: Path, show_answer: Callable[[int, Any], None]):
    top, bottom = path.read_text().split("\n\n")
    ordering_rules = set(tuple(map(int, x.split("|"))) for x in top.split())
    pages_to_produce = tuple(tuple(map(int, x.split(","))) for x in bottom.split())

    part1 = 0
    part2 = 0
    for pages in pages_to_produce:
        sorted_pages = tuple(
            sorted(
                pages,
                key=cmp_to_key(lambda x, y: -1 if (x, y) in ordering_rules else 1),
            )
        )
        if pages == sorted_pages:
            part1 += pages[len(pages) // 2]
        else:
            part2 += sorted_pages[len(sorted_pages) // 2]

    show_answer(1, part1)
    show_answer(2, part2)


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    print(f"Advent of Code {year} Day {day}")
    print("=" * 80)
    get_input_file(year, day)
    if not INPUT_FILE.exists():
        return
    show_answer: Callable[[int, Any], None] = lambda part, answer: print(
        f"Answer Part {part}: {answer or ''}", "=" * 80, sep="\n"
    )
    solve(INPUT_FILE, show_answer)
    # solve_v2(INPUT_FILE, show_answer)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
