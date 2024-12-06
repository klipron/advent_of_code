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
    text = path.read_text()
    ordering_rules, pages_to_produce = text.split("\n\n")
    ordering_rules = set(tuple(map(int, z.split("|"))) for z in ordering_rules.split())
    pages_to_produce = tuple(
        tuple(map(int, z.split(","))) for z in pages_to_produce.split()
    )
    part1 = 0
    part2 = 0
    for pages in pages_to_produce:
        page_rules = []
        for i, page in enumerate(pages):
            for next_page in pages[i + 1 :]:
                page_rules.append((page, next_page))
        if all(x in ordering_rules for x in page_rules):
            part1 += pages[len(pages) // 2]
        else:
            rules = set()
            for rule in ordering_rules:
                if all(x in pages for x in rule):
                    rules.add(rule)
            new_ordering = []
            for page in pages:
                if not new_ordering:
                    new_ordering.append(page)
                    continue
                for ii, ordered_page in enumerate(new_ordering):
                    if (page, ordered_page) in rules:
                        new_ordering.insert(ii, page)
                        break
                else:
                    new_ordering.append(page)
            part2 += new_ordering[len(pages) // 2]

    show_answer(1, part1)
    show_answer(2, part2)


def solve_v2(path: Path, show_answer: Callable[[int, Any], None]):
    parts = path.read_text().split("\n\n")
    ordering_rules = set(tuple(map(int, x.split("|"))) for x in parts[0].split())
    pages_to_produce = tuple(tuple(map(int, x.split(","))) for x in parts[1].split())

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
    solve_v2(INPUT_FILE, show_answer)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
