import os
import collections

KEY_FILE = "key.txt"
INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def get_input_file(*, day: int, input_file: str = INPUT_FILE, key_file: str = KEY_FILE):
    with open(key_file) as f:
        key = f.read()
    os.system(
        f'curl -b "session={key}" https://adventofcode.com/2023/day/{day}/input > {input_file}'
    )


def part1(filename: str):
    total = 0
    with open(filename) as f:
        for line in f.readlines():
            winning_nums, your_nums = line.split(":")[1].split("|")
            matches = len(set(winning_nums.split()).intersection(your_nums.split()))
            total += 1 << matches - 1 if matches else 0
    return total


def part2(filename: str):
    with open(filename) as f:
        cards: collections.defaultdict[int, int] = collections.defaultdict(int)
        for i, line in enumerate(f.readlines(), start=1):
            winning_nums, your_nums = line.split(":")[1].split("|")
            matches = len(set(winning_nums.split()) & set(your_nums.split()))
            cards[i] += 1
            for x in range(1, matches + 1):
                cards[i + x] = cards.get(i + x, 0) + cards[i]
    return sum(cards.values())


def main():
    print("Advent of Code Day 4")
    input_file = INPUT_FILE
    if not os.path.exists(input_file):
        get_input_file(day=4)
        if not os.path.exists(input_file):
            return print("Failed to fetch input file.")
    print(f"Answer Part 1: {part1(input_file) or ''}")
    print(f"Answer Part 2: {part2(input_file) or ''}")


if __name__ == "__main__":
    main()
