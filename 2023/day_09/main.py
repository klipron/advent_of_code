import os
from datetime import datetime

KEY_FILE = "key.txt"
INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def get_input_file(
    *, advent_date: datetime, input_file: str = INPUT_FILE, key_file: str = KEY_FILE
):
    with open(key_file) as f:
        key = f.read()
    os.system(
        f'curl -b "session={key}" https://adventofcode.com/{advent_date.year}/day/{advent_date.day}/input > {input_file}'
    )


def parse_file(filename: str):
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            yield map(int, line.strip().split())


def get_next_value(*nums, add_to_start=False):
    diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    if not any(diffs):
        return nums[-1]
    if add_to_start:
        return nums[0] - get_next_value(*diffs, add_to_start=add_to_start)
    return nums[-1] + get_next_value(*diffs, add_to_start=add_to_start)


def part1(filename: str):
    data = parse_file(filename)
    return sum(get_next_value(*nums) for nums in data)


def part2(filename: str):
    data = parse_file(filename)
    return sum(get_next_value(*nums, add_to_start=True) for nums in data)


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
