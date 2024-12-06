import os
import re
import ssl
import time
from pathlib import Path
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request
from typing import Callable, Any, NamedTuple

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


def show_answer(*, part: int, answer: int):
    print(f"Answer Part {part}: {answer or ''}", "=" * 80, sep="\n")


Grid = dict["Position", str]


class Position(NamedTuple):
    x: int
    y: int

    def move_up(self):
        return Position(self.x, self.y - 1)

    def move_down(self):
        return Position(self.x, self.y + 1)

    def move_left(self):
        return Position(self.x - 1, self.y)

    def move_right(self):
        return Position(self.x + 1, self.y)


class Guard:
    def __init__(self, position: Position, direction: str) -> None:
        self.position = position
        self.last_point = None
        self.direction = direction

    def move(self):
        self.last_point = self.position
        moves = {
            "^": Position.move_up,
            "v": Position.move_down,
            "<": Position.move_left,
            ">": Position.move_right,
        }
        self.position = moves[self.direction](self.position)

    def turn(self):
        self.position = self.last_point
        self.direction = {"^": ">", "v": "<", "<": "^", ">": "v"}[self.direction]


def get_grid(path: Path):
    grid: Grid = {}
    for ridx, line in enumerate(path.open().readlines()):
        for cidx, char in enumerate(line.strip()):
            grid[Position(cidx, ridx)] = char
    return grid


def get_guard_path(grid: Grid, guard: Guard):
    while guard.position in grid:
        if grid[guard.position] == "#":
            guard.turn()
        else:
            yield guard.position, guard.direction
        guard.move()


def solve(path: Path):
    grid = get_grid(path)
    starting_position = next(p for p, c in grid.items() if c not in ("#", "."))
    guard = Guard(starting_position, grid[starting_position])
    seen_positions = set(p for p, _ in get_guard_path(grid, guard))
    total_seen_positions = len(seen_positions)

    show_answer(part=1, answer=total_seen_positions)

    total = 0
    for i, pos in enumerate(seen_positions):
        if pos == starting_position:
            continue
        print(f"Checked {i+1} of {total_seen_positions}...".ljust(50), end="\r")
        grid = get_grid(path)
        guard = Guard(starting_position, grid[starting_position])
        grid[pos] = "#"
        seen = set()
        for guard_pos in get_guard_path(grid, guard):
            if guard_pos in seen:
                break
            seen.add(guard_pos)
        else:
            continue
        total += 1
    print(f"Checked {i+1} of {total_seen_positions}.".ljust(50))
    show_answer(part=2, answer=total)


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
