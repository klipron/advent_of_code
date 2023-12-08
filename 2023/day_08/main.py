import os, functools
from datetime import datetime
from math import lcm, gcd

KEY_FILE = "key.txt"
INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def get_input_file(*, day: int, input_file: str = INPUT_FILE, key_file: str = KEY_FILE):
    with open(key_file) as f:
        key = f.read()
    os.system(
        f'curl -b "session={key}" https://adventofcode.com/2023/day/{day}/input > {input_file}'
    )


def parse_file(filename: str):
    with open(filename) as f:
        nodes: dict[str, tuple[str, str]] = {}
        instructions: str = []
        for i, line in enumerate(f.readlines()):
            line = line.strip()
            if not line:
                continue
            if i == 0:
                instructions = line
                continue
            left, right = line.split("=")
            nodes[left.strip()] = tuple(
                x.strip() for x in right.strip().strip("()").split(",")
            )
    return instructions, nodes


def part1(filename: str):
    instructions, nodes = parse_file(filename)

    steps = 0
    current_node = "AAA"
    FINAL_NODE = "ZZZ"
    while current_node != FINAL_NODE:
        for i in instructions:
            if current_node == FINAL_NODE:
                break
            current_node = nodes[current_node]["LR".index(i)]
            steps += 1
    return steps


def part2(filename: str):
    instructions, nodes = parse_file(filename)

    end_node_steps: list[int] = []
    for node in nodes.keys():
        if not node.endswith("A"):
            continue
        steps = 0
        while not node.endswith("Z"):
            for i in instructions:
                steps += 1
                node = nodes[node]["LR".index(i)]
                if node.endswith("Z"):
                    end_node_steps.append(steps)
                    break
    # Other way to calculate LCM
    # return functools.reduce(lambda x, y: (x * y) // gcd(x, y), end_node_steps)
    return lcm(*end_node_steps)


def main():
    day = int(os.path.split(os.path.dirname(__file__))[1].split("_")[1])
    year = os.path.split(os.path.split(os.path.dirname(__file__))[0])[1]
    advent_date = datetime(int(year), 12, day)
    print(f"Advent of Code Day {advent_date.day}")
    print("=" * 80)
    if advent_date > datetime.now():
        print(
            f"Today's challenge is not ready as yet please try again in {advent_date - datetime.now()}"
        )
        return
    input_file = INPUT_FILE
    if not os.path.exists(input_file):
        get_input_file(advent_date=advent_date)
        if not os.path.exists(input_file):
            return print("Failed to fetch input file.")
    print(f"Answer Part 1: {part1(input_file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(input_file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
