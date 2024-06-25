from enum import IntEnum
from pathlib import Path
from datetime import date
from typing import Self, Callable
from http.client import HTTPResponse
from urllib.request import urlopen, Request

import heapq

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


class Direction(IntEnum):
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2


class Node:
    def __init__(
        self,
        pos: tuple[int, int],
        value: int,
        direction: Direction | None = None,
        direction_count=0,
        prev_pos=None,
        is_ultra=False,
    ) -> None:
        self.pos = pos
        self.prev_pos = prev_pos
        self.value = value
        self.direction = direction
        self.direction_count = direction_count
        self.is_ultra = is_ultra

    def __repr__(self) -> str:
        return f"Node(pos={self.pos}, value={self.value}, direction={self.direction}, direction_count={self.direction_count})"

    def __hash__(self) -> int:
        return hash(
            (
                self.pos,
                self.prev_pos,
                self.direction if self.direction is not None else 0,
                self.direction_count,
            )
        )

    def __eq__(self, other) -> bool:
        assert isinstance(other, self.__class__)
        return hash(self) == hash(other)

    def __lt__(self, other: Self):
        assert isinstance(other, self.__class__)
        return self.value < other.value

    def move(self, direction: Direction):
        x, y = self.pos
        if direction == Direction.UP:
            return (x, y - 1)
        elif direction == Direction.DOWN:
            return (x, y + 1)
        elif direction == Direction.LEFT:
            return (x - 1, y)
        elif direction == Direction.RIGHT:
            return (x + 1, y)

    def iter_children(
        self,
        get_value: Callable[[tuple[int, int]], int | None],
    ):
        for direction in (
            Direction.UP,
            Direction.DOWN,
            Direction.LEFT,
            Direction.RIGHT,
        ):
            if self.direction is not None:
                if direction == self.direction * -1:
                    continue
                if (
                    not self.is_ultra
                    and self.direction == direction
                    and self.direction_count >= 3
                ):
                    continue
                if self.is_ultra and (
                    (self.direction != direction and self.direction_count < 4)
                    or (self.direction == direction and self.direction_count >= 10)
                ):
                    continue
            child_pos = self.move(direction)
            value = get_value(child_pos)
            if value is None:
                continue
            yield Node(
                child_pos,
                self.value + value,
                direction,
                self.direction_count + 1 if self.direction == direction else 1,
                self.pos,
                self.is_ultra,
            )


def get_grid(path: Path):
    grid: dict[tuple[int, int], int] = {}
    for y, line in enumerate(path.open().readlines()):
        for x, num in enumerate(line.strip()):
            grid[(x, y)] = int(num)

    return grid


def get_min_heat_loss(path: Path, *, is_ultra=False):
    grid = get_grid(path)
    start_pos = min(grid.keys())
    last_pos = max(grid.keys())
    get_value: Callable[[tuple[int, int]], int | None] = lambda pos: grid.get(pos)

    seen_nodes: set[Node] = set()
    nodes: list[Node] = [Node(start_pos, 0, is_ultra=is_ultra)]

    while nodes:
        node = heapq.heappop(nodes)
        seen_nodes.add(node)
        for child in node.iter_children(get_value):
            if child.pos == last_pos:
                return child.value
            if child in seen_nodes:
                continue
            heapq.heappush(nodes, child)
            seen_nodes.add(child)
        print(f"{node.pos} {node.value}", end="\r")


def part1(path: Path):
    return get_min_heat_loss(path)


def part2(path: Path):
    return get_min_heat_loss(path, is_ultra=True)


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
    get_input_file(advent_date)
    file = INPUT_FILE
    print(f"Answer Part 1: {part1(file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
