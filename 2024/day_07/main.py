import os
import ssl
import time
import functools
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


@functools.lru_cache
def int_to_base(num: int, *, length: int, base: int):
    values = ()
    while num:
        num, rem = divmod(num, base)
        values += (rem,)
    text = "".join(map(str, reversed(values))).rjust(length, "0")
    return map(int, text)


@functools.lru_cache
def get_operators(*, length: int, base: int):
    return tuple(
        tuple(x for x in int_to_base(i, length=length, base=base))
        for i in range(int(str(base - 1) * length, base=base) + 1)
    )


def get_calibration_results(
    equations: list[tuple[int, tuple[int, ...]]],
    operator_functions: tuple[Callable[[int, int], int], ...],
):
    total = 0
    total_equations = len(equations)
    for idx, (test_result, values) in enumerate(equations, start=1):
        print(f"{idx} of {total_equations}: {total}", end="\r")
        for operators in get_operators(
            length=len(values) - 1, base=len(operator_functions)
        ):
            result = values[0]
            for i, operator_index in enumerate(operators, start=1):
                result = operator_functions[operator_index](result, values[i])
                if result > test_result:
                    break
            else:
                if result == test_result:
                    total += test_result
                    break

            # This version of applying operators uses reduce but is 10 secs slower.
            # operators = (operator_functions[x] for x in operators)
            # result = functools.reduce(
            #     lambda acc, val: next(operators)(acc, val), values
            # )

    return total


def solve(path: Path):
    equations: list[tuple[int, tuple[int, ...]]] = []
    for line in path.open().readlines():
        key, value = line.strip().split(":")
        equations.append((int(key), tuple(map(int, value.strip().split()))))

    funcs = (int.__add__, int.__mul__)
    show_answer(part=1, answer=get_calibration_results(equations, funcs))

    funcs += (lambda x, y: int(str(x) + str(y)),)
    show_answer(part=2, answer=get_calibration_results(equations, funcs))


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


def show_answer(*, part: int, answer: int):
    print(f"Answer Part {part}: {answer or ''}".ljust(50), "=" * 80, sep="\n")


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
