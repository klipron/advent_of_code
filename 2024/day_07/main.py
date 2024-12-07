import os
import re
import ssl
import time
import functools
from pathlib import Path
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request
from typing import Callable, Any, NamedTuple

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


def show_answer(*, part: int, answer: int):
    print(f"Answer Part {part}: {answer or ''}".ljust(50), "=" * 80, sep="\n")


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


def int_to_base(num: int, *, base: int):
    value = ""
    while num:
        num, rem = divmod(num, base)
        value = str(rem) + value
    return value


def get_operators(*, length: int, funcs: tuple[Callable, ...]):
    base = len(funcs)
    for i in range(int(str(base - 1) * length, base=base) + 1):
        yield (funcs[int(x)] for x in int_to_base(i, base=base).rjust(length, "0"))


def get_calibration_results(
    equations: list[tuple[int, tuple[int, ...]]],
    operator_functions: tuple[Callable, ...],
):
    total = 0
    total_equations = len(equations)
    for idx, (test_result, values) in enumerate(equations, start=1):
        print(f"{idx} of {total_equations}: {total}", end="\r")
        for operators in get_operators(
            length=len(values) - 1, funcs=operator_functions
        ):
            acc = values[0]
            for i, op in enumerate(operators, start=1):
                acc = op(acc, values[i])
            if acc == test_result:
                total += test_result
                break
    return total


def solve(path: Path):
    equations: list[tuple[int, tuple[int, ...]]] = []
    for line in path.open().readlines():
        key, value = line.strip().split(":")
        equations.append((int(key), tuple(map(int, value.strip().split()))))

    show_answer(
        part=1, answer=get_calibration_results(equations, (int.__add__, int.__mul__))
    )

    show_answer(
        part=2,
        answer=get_calibration_results(
            equations, (int.__add__, int.__mul__, lambda x, y: int(str(x) + str(y)))
        ),
    )


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    print(f"Advent of Code {year} Day {day}")
    print("=" * 80)
    get_input_file(year, day)
    if not INPUT_FILE.exists():
        return
    solve(INPUT_FILE)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
