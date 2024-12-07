import os
import ssl
import time
from pathlib import Path
from typing import NamedTuple
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


def show_answer(*, part: int, answer: int):
    print(f"Answer Part {part}: {answer or ''}".ljust(50), "=" * 80, sep="\n")


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
    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.position = next(p for p, c in grid.items() if c not in ("#", "."))
        self.last_position = None
        self.direction = self.grid[self.position]
        self._moves = {
            "^": Position.move_up,
            "v": Position.move_down,
            "<": Position.move_left,
            ">": Position.move_right,
        }
        self._turns = {"^": ">", "v": "<", "<": "^", ">": "v"}

    def move(self):
        self.last_position = self.position
        self.position = self._moves[self.direction](self.position)

    def turn(self):
        self.position = self.last_position
        self.direction = self._turns[self.direction]

    def patrol(self):
        while self.position in self.grid:
            if self.grid[self.position] == "#":
                self.turn()
            else:
                yield self.position, self.direction
            self.move()


def get_grid(path: Path):
    grid: Grid = {}
    with path.open() as fp:
        ridx = 0
        while line := fp.readline():
            for cidx, char in enumerate(line.strip()):
                grid[Position(cidx, ridx)] = char
            ridx += 1
    return grid


def solve(path: Path):
    grid = get_grid(path)
    guard = Guard(grid)
    seen_positions = set(pos for pos, _ in guard.patrol())
    total_seen_positions = len(seen_positions)
    show_answer(part=1, answer=total_seen_positions)

    loops_found = 0
    last_seen_position = None
    for i, seen_position in enumerate(seen_positions):
        if grid[seen_position] != ".":
            continue
        if last_seen_position is not None:
            grid[last_seen_position] = "."
        last_seen_position = seen_position
        grid[seen_position] = "#"
        print(
            f"Checked {i+1} of {total_seen_positions}: {loops_found} loops found.".ljust(
                50
            ),
            end="\r",
        )
        guard = Guard(grid)
        seen = set()
        for guard_position in guard.patrol():
            if guard_position in seen:
                break
            seen.add(guard_position)
        else:
            continue
        loops_found += 1
    show_answer(part=2, answer=loops_found)


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
