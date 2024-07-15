import time
import enum
from pathlib import Path
from datetime import date
from typing import NamedTuple
from collections import defaultdict
from http.client import HTTPResponse
from urllib.request import urlopen, Request

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


class Direction(enum.IntEnum):
    UP = -1
    DOWN = 1
    LEFT = 2
    RIGHT = -2


class Tile(NamedTuple):
    x: int
    y: int


class Trail:
    def __init__(
        self,
        starting_tile: Tile,
        seen_tiles: set[Tile] | None = None,
        direction: Direction = None,
        total=0,
    ) -> None:
        self.last_tile = starting_tile
        self.direction = direction
        self.seen_tiles = set() if seen_tiles is None else seen_tiles
        self.total = total


def get_grid(path: Path):
    grid: dict[Tile, str] = {}
    for y, line in enumerate(path.open().readlines()):
        for x, char in enumerate(line.strip()):
            grid[Tile(x, y)] = char
    return grid


def move(tile: Tile, direction: Direction | None = None):
    moves = {
        Direction.UP: Tile(tile.x, tile.y - 1),
        Direction.DOWN: Tile(tile.x, tile.y + 1),
        Direction.LEFT: Tile(tile.x - 1, tile.y),
        Direction.RIGHT: Tile(tile.x + 1, tile.y),
    }
    if direction is not None:
        yield moves[direction], direction
    else:
        for direction in (
            Direction.UP,
            Direction.DOWN,
            Direction.LEFT,
            Direction.RIGHT,
        ):
            yield moves[direction], direction


def display_grid(
    grid: dict[Tile, str], starting_tile: Tile, seen_tiles: set[Tile], *, symbol="O"
):
    rows = defaultdict(list)
    for tile, c in grid.items():
        rows[tile.y].append(
            "S" if tile == starting_tile else symbol if tile in seen_tiles else c
        )
    for row in rows.values():
        print("".join(row))


def part1(path: Path):
    grid = get_grid(path)
    max_point = max(grid)
    starting_tile = next(tile for tile, c in grid.items() if tile.y == 0 and c == ".")
    ending_tile = next(
        tile for tile, c in grid.items() if tile.y == max_point.y and c == "."
    )

    slopes = {
        "^": Direction.UP,
        "v": Direction.DOWN,
        "<": Direction.LEFT,
        ">": Direction.RIGHT,
    }
    trails: list[Trail] = [Trail(starting_tile)]
    trail_lengths = []
    while trails:
        trail = trails.pop()
        while trail.last_tile != ending_tile:
            next_positions: list[tuple[int, int]] = []
            for next_tile, next_dir in move(trail.last_tile):
                if next_tile == starting_tile:
                    continue
                char = grid.get(next_tile)
                if char is None:
                    continue
                if next_tile in trail.seen_tiles:
                    continue
                if char in slopes:
                    direction = slopes[char]
                    if next_dir == direction * -1:
                        continue
                    seen = trail.seen_tiles.copy()
                    seen.add(next_tile)
                    next_tile, d = next(move(next_tile, direction))
                    char = grid.get(next_tile)
                    if char is None or char == "#":
                        continue
                    seen.add(next_tile)
                    trails.append(Trail(next_tile, seen, d))
                    continue
                if char == "#":
                    continue
                next_positions.append(next_tile)
            if not next_positions:
                break
            for i, next_tile in enumerate(next_positions):
                trail.seen_tiles.add(next_tile)
                if i == 0:
                    trail.last_tile = next_tile
                else:
                    trails.append(Trail(next_tile, trail.seen_tiles))
        if trail.last_tile == ending_tile:
            trail_lengths.append(len(trail.seen_tiles))

    return max(trail_lengths)


def part2(path: Path):
    grid = get_grid(path)
    max_tile = max(grid)
    is_tile = lambda char: char is not None and char != "#"
    starting_tile = next(tile for tile, c in grid.items() if tile.y == 0 and is_tile(c))
    ending_tile = next(
        tile for tile, c in grid.items() if tile.y == max_tile.y and is_tile(c)
    )

    intersection_tiles: set[Tile] = set([starting_tile, ending_tile])
    for tile, char in grid.items():
        if not is_tile(char):
            continue
        if sum(1 for x, _ in move(tile) if not is_tile(grid.get(x))) < 2:
            intersection_tiles.add(tile)

    intersection_trails = defaultdict(list)
    for intersection_tile in intersection_tiles:
        for option_tile, _ in move(intersection_tile):
            if not is_tile(grid.get(option_tile)):
                continue
            trail = Trail(option_tile, set([intersection_tile, option_tile]))
            while True:
                for next_tile, _ in move(trail.last_tile):
                    if (
                        not is_tile(grid.get(next_tile))
                        or next_tile in trail.seen_tiles
                    ):
                        continue
                    if next_tile in intersection_tiles:
                        if next_tile == ending_tile:
                            trail.seen_tiles.add(next_tile)
                            intersection_trails[intersection_tile].append(
                                (next_tile, len(trail.seen_tiles))
                            )
                        else:
                            intersection_trails[intersection_tile].append(
                                (next_tile, len(trail.seen_tiles))
                            )
                        break
                    trail.last_tile = next_tile
                    trail.seen_tiles.add(next_tile)
                else:
                    continue
                break

    totals = []
    trails = [Trail(starting_tile)]
    while trails:
        trail = trails.pop()
        for tile, total in intersection_trails[trail.last_tile]:
            if tile in trail.seen_tiles:
                continue
            new_total = trail.total + total
            if tile == ending_tile:
                totals.append(new_total - 1)
                continue
            seen = trail.seen_tiles.copy()
            seen.add(tile)
            trails.append(Trail(tile, seen, total=new_total))

    return max(totals)


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
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
