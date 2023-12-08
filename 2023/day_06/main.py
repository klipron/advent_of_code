import os, math, cmath
import collections

KEY_FILE = "key.txt"
INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def quad_equation(*, a: int = 1, b: int, c: int):
    # If a is 0, then incorrect equation
    if a == 0:
        return print("Input correct quadratic equation")
    # calculating discriminant using formula
    dis = b * b - 4 * a * c
    sqrt_val = math.sqrt(abs(dis))

    return ((-b + sqrt_val) / (2 * a).real, (-b - sqrt_val) / (2 * a).real)


def quad_equation2(*, a: int = 1, b: int, c: int):
    # If a is 0, then incorrect equation
    if a == 0:
        return print("Input correct quadratic equation")
    dis = (b**2) - (4 * a * c)

    # find two results
    ans1 = (-b - cmath.sqrt(dis)) / (2 * a)
    ans2 = (-b + cmath.sqrt(dis)) / (2 * a)

    return (ans1.real, ans2.real)


def get_input_file(*, day: int, input_file: str = INPUT_FILE, key_file: str = KEY_FILE):
    with open(key_file) as f:
        key = f.read()
    os.system(
        f'curl -b "session={key}" https://adventofcode.com/2023/day/{day}/input > {input_file}'
    )


def parse_file(filename: str):
    times = []
    distances = []
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            nums = map(int, line.split(":")[1].strip().split())
            if line.startswith("Time:"):
                times += nums
            if line.startswith("Distance:"):
                distances += nums

    return zip(times, distances)


def part1(filename: str):
    total = 1
    for time, dist in parse_file(filename):
        print((time, dist))
        error_margin = 0
        for hold in range(1, time):
            curr_dist = (time - hold) * hold
            if curr_dist > dist:
                error_margin += 1
        print(error_margin)
        print("=" * 80)
        total *= error_margin
    return total


def part2(filename: str):
    data = parse_file(filename)

    time, dist = tuple((int("".join(map(str, x))) for x in zip(*data)))

    result = quad_equation(a=1, b=-time, c=dist)
    # result = quad_equation2(a=1, b=-time, c=dist)
    x, y = map(int, result)
    return abs(y - x)


def main():
    print("Advent of Code Day 6")
    input_file = INPUT_FILE
    if not os.path.exists(input_file):
        get_input_file(day=6)
        if not os.path.exists(input_file):
            return print("Failed to fetch input file.")
    print("=" * 80)
    print(f"Answer Part 1: {part1(input_file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(input_file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
