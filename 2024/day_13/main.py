import time

start = time.time()

import os
import re
import ssl
from pathlib import Path
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


X = "x"
Y = "y"
A = "a"
B = "b"


def get_machines(path: Path):
    for lines in path.read_text().split("\n\n"):
        machine = {"buttons": {}}
        for line in lines.splitlines():
            if result := re.match(r"Button ([A,B]): (X)\+(\d+)\, (Y)\+(\d+)", line):
                result = result.groups()
                machine["buttons"][str.lower(result[0])] = dict(
                    (
                        (str.lower(result[1]), int(result[2])),
                        (str.lower(result[3]), int(result[4])),
                    )
                )
            elif result := re.match(r"Prize: (X)=(\d+)\, (Y)=(\d+)", line):
                result = result.groups()
                machine["prize"] = dict(
                    (
                        (str.lower(result[0]), int(result[1])),
                        (str.lower(result[2]), int(result[3])),
                    )
                )
        yield machine


def solve(path: Path, test=False):
    machines = tuple(get_machines(path))

    total_tokens = 0
    for machine in machines:
        btn_A = machine["buttons"][A]
        btn_B = machine["buttons"][B]
        prize = machine["prize"]
        tokens = []
        for val_A in range((prize[X] // btn_A[X]) + 1):
            val_B, rem = divmod((prize[X] - (val_A * btn_A[X])), btn_B[X])
            if rem:
                continue
            if val_A and (btn_A[Y] * val_A) + (btn_B[Y] * val_B) == prize[Y]:
                tokens.append((val_A * 3) + val_B)
        total_tokens += min(tokens) if tokens else 0
    print("Answer using Naive method")
    show_answer(part=1, answer=total_tokens, test=test)

    for conversion in (0, 10000000000000):
        total_tokens = 0
        for machine in machines:
            btn_A = machine["buttons"][A]
            btn_B = machine["buttons"][B]
            prize = machine["prize"]
            prize[X] += conversion
            prize[Y] += conversion

            val_B, rem = divmod(
                (btn_A[Y] * prize[X]) - (btn_A[X] * prize[Y]),
                (btn_A[Y] * btn_B[X]) - (btn_A[X] * btn_B[Y]),
            )
            if rem:
                continue
            val_A, rem = divmod(prize[X] - (btn_B[X] * val_B), btn_A[X])
            if rem:
                continue
            total_tokens += (val_A * 3) + val_B
        print("Answer calculated using a formula")
        if not conversion:
            show_answer(part=1, answer=total_tokens, test=test)
        else:
            show_answer(part=2, answer=total_tokens, test=test)


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
