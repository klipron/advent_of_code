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
    max_cubes = {"red": 12, "green": 13, "blue": 14}
    with open(filename) as f:
        for line in f.readlines():
            valid_game = True
            game, data = line.split(":")
            for sub_game in data.split(";"):
                for cube in sub_game.split(","):
                    count, colour = cube.split()
                    if int(count) > max_cubes.get(colour, 0):
                        valid_game = False
            if valid_game:
                total += int(game.split()[1])
    return total


def part2(filename: str):
    total = 0
    colours = ("red", "green", "blue")
    with open(filename) as f:
        for line in f.readlines():
            _, data = line.split(":")
            sub_total = 1
            for colour in colours:
                max_colour_cubes = 1
                for sub_game in data.split(";"):
                    cubes = [x.split() for x in sub_game.split(",")]
                    max_cubes = max(
                        [
                            int(count)
                            for count, cube_colour in cubes
                            if cube_colour == colour
                        ]
                        or [0]
                    )
                    if max_cubes > max_colour_cubes:
                        max_colour_cubes = max_cubes
                sub_total *= max_colour_cubes
            total += sub_total
    return total


def main():
    print("Advent of Code Day 2")
    input_file = INPUT_FILE
    if not os.path.exists(input_file):
        get_input_file(day=2)
        if not os.path.exists(input_file):
            return print("Failed to fetch input file.")
    print(f"Answer Part 1: {part1(input_file) or ''}")
    print(f"Answer Part 2: {part2(input_file) or ''}")


if __name__ == "__main__":
    main()
