import os

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
            first = next(x for x in line if x.isdigit())
            last = next(x for x in line[::-1] if x.isdigit())
            total += int(first + last)
    return total


def part2(filename: str):
    num_words = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    total = 0
    with open(filename) as f:
        for line in f.readlines():
            first_index, first_num = next(
                ((i, x) for i, x in enumerate(line) if x.isdigit()), (None, None)
            )
            last_index, last_num = next(
                ((i, x) for i, x in enumerate(line[::-1]) if x.isdigit()), (None, None)
            )

            for i, k in enumerate(num_words):
                if k not in line:
                    continue
                word_first_index = line.index(k)
                if first_index is None or word_first_index < first_index:
                    first_index = word_first_index
                    first_num = str(i)
                word_last_index = line[::-1].index(k[::-1])
                if last_index is None or word_last_index < last_index:
                    last_index = word_last_index
                    last_num = str(i)
            total += int(first_num + last_num)
    return total


def main():
    print("Advent of Code Day 1")
    input_file = INPUT_FILE
    if not os.path.exists(input_file):
        get_input_file(day=1)
        if not os.path.exists(input_file):
            return print("Failed to fetch input file.")
    print(f"Answer Part 1: {part1(input_file) or ''}")
    print(f"Answer Part 2: {part2(input_file) or ''}")


if __name__ == "__main__":
    main()
