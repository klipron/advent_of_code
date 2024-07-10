import re
from pathlib import Path
from datetime import date
from typing import NamedTuple
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


def get_workflows(lines: list[str]):
    workflows: dict[str, list[str]] = {}
    for line in lines:
        result = re.match(r"(?P<p1>.+){(?P<p2>.+)}", line.strip())
        assert result is not None
        name, rules = result.groups()
        workflows[name] = rules.split(",")
    return workflows


def get_parts(lines: list[str]):
    return [re.findall(r"\w=\d+", line.strip()) for line in lines]


def process_rules(rules: list[str], part: list[str]):
    for part_rating in part:
        exec(part_rating)
    for rule in rules:
        if ":" in rule:
            condition, result = rule.split(":")
            if eval(condition):
                return result
        else:
            return rule


def part1(path: Path):
    lines = path.open().readlines()
    partition = lines.index("\n")
    workflows = get_workflows(lines[:partition])
    parts = get_parts(lines[partition + 1 :])

    accepted: list[str] = []

    for part in parts:
        workflow_name = "in"
        while True:
            rules = workflows[workflow_name]
            result = process_rules(rules, part)
            assert result is not None
            if result == "A":
                accepted.append(part)
                break
            if result == "R":
                break
            workflow_name = result

    return sum(sum(map(int, re.findall(r"\d+", "".join(part)))) for part in accepted)


class Part(NamedTuple):
    x: tuple[int, int] = (1, 4000)
    m: tuple[int, int] = (1, 4000)
    a: tuple[int, int] = (1, 4000)
    s: tuple[int, int] = (1, 4000)

    def __repr__(self) -> str:
        return f"Part(x={self.x}, m={self.m}, a={self.a}, s={self.s})"

    def total(self):
        total = 1
        for attr in ("x", "m", "a", "s"):
            _min, _max = getattr(self, attr)
            total *= _max - (_min - 1)
        return total


def part2(path: Path):
    lines = path.open().readlines()
    partition = lines.index("\n")
    workflows = get_workflows(lines[:partition])

    parts = [("in", Part())]
    accepted_parts: set[Part] = set()

    while parts:
        workflow, part = parts.pop()
        rules = workflows[workflow]
        for rule in rules:
            if rule == "A":
                accepted_parts.add(part)
            elif rule == "R":
                continue
            elif result := re.match(
                r"(?P<p1>[xmas])(?P<p2>[<>])(?P<p3>\d+):(?P<p4>\w+)", rule
            ):
                attr, sign, val, next_workflow = result.groups()
                val = int(val)
                _min, _max = getattr(part, attr)
                assert _max > _min
                assert int(val) in range(_min, _max + 1)
                if sign == "<":
                    new_part = part._replace(**{attr: (_min, val - 1)})
                    if next_workflow == "A":
                        accepted_parts.add(new_part)
                    elif next_workflow != "R":
                        parts.append((next_workflow, new_part))
                    part = part._replace(**{attr: (val, _max)})
                elif sign == ">":
                    new_part = part._replace(**{attr: (val + 1, _max)})
                    if next_workflow == "A":
                        accepted_parts.add(new_part)
                    elif next_workflow != "R":
                        parts.append((next_workflow, new_part))
                    part = part._replace(**{attr: (_min, val)})
                else:
                    raise ValueError(f"Invalid value {sign}.")
            else:
                parts.append((rule, part))

    return sum(x.total() for x in accepted_parts)


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
    file = TEST_FILE
    print(f"Answer Part 1: {part1(file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
