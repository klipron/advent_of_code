import time
from typing import NamedTuple

start = time.time()

import os
import ssl
import functools
from pathlib import Path
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


class Robot(NamedTuple):
    x: int
    y: int
    dx: int
    dy: int

    def move(self, grid_width: int, grid_height: int):
        x = self.x + self.dx
        y = self.y + self.dy
        if x >= grid_width:
            x -= grid_width
        elif x < 0:
            x = grid_width + x
        if y >= grid_height:
            y -= grid_height
        elif y < 0:
            y = grid_height + y
        return Robot(x, y, self.dx, self.dy)


def solve(path: Path, test=False):
    robots: list[Robot] = []
    for line in path.open():
        data = []
        for part in line.split():
            data.extend(map(int, part.split("=")[1].split(",")))
        robots.append(Robot(*data))

    w, h = (11, 7) if test else (101, 103)
    mw, mh = w // 2, h // 2

    q1, q2, q3, q4 = [()] * 4
    for robot in robots:
        for _ in range(100):
            robot = robot.move(w, h)
        if robot.x < mw and robot.y < mh:
            q1 += (robot,)
        elif robot.x > mw and robot.y < mh:
            q2 += (robot,)
        elif robot.x < mw and robot.y > mh:
            q3 += (robot,)
        elif robot.x > mw and robot.y > mh:
            q4 += (robot,)

    show_answer(
        part=1,
        answer=functools.reduce(int.__mul__, map(len, (q1, q2, q3, q4))),
        test=test,
    )

    christmas_tree_options = []
    for i in range(mh):
        options = set()
        for y in range(h):
            if y < i:
                continue
            if y == i:
                options.add((mw, y))
                continue
            l, r = mw + i - y, mw - i + y
            if r >= w:
                break
            options.add((l, y))
            options.add((r, y))
        christmas_tree_options.append(options)

    matched_positions = []
    for i in range(w * h):
        print(i, end="\r")
        positions = []
        new_robots_positions = []
        for robot in robots:
            new_robot = robot.move(w, h)
            positions.append((robot.x, robot.y))
            new_robots_positions.append(new_robot)
        for options in christmas_tree_options:
            matched_positions.append((len(set.intersection(options, positions)), i))
        robots = new_robots_positions

    show_answer(part=2, answer=max(matched_positions)[1], test=test)


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
