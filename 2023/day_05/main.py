import os
from collections import defaultdict

KEY_FILE = "key.txt"
INPUT_FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def get_input_file(*, day: int, input_file: str = INPUT_FILE, key_file: str = KEY_FILE):
    with open(key_file) as f:
        key = f.read()
    os.system(
        f'curl -b "session={key}" https://adventofcode.com/2023/day/{day}/input > {input_file}'
    )


def parse_file(filename):
    with open(filename) as f:
        seed_map: dict[str, list[list[str]]] = {}
        current_map = ""
        seeds = []
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("seeds"):
                seeds += [int(x) for x in line.split(":")[1].split()]
                continue
            if line.endswith("map:"):
                current_map = line.split()[0]
                seed_map[current_map] = []
                continue
            seed_map[current_map].append(tuple(int(x) for x in line.split()))
    return seeds, seed_map


def part1(filename: str = INPUT_FILE):
    seeds, seed_maps = parse_file(filename)
    print(seeds)
    print("=" * 80)

    locations = []
    seed_locations = {}
    for seed in seeds:
        print("Seed: ", seed)
        current_value = seed
        next_value = None
        for key in seed_maps.keys():
            current_value = next_value or current_value
            for dest, source, length in seed_maps[key]:
                if not (current_value >= source and current_value <= source + length):
                    continue
                next_value = dest + (current_value - source)
                break
            print(f"{key}: {next_value or current_value}")
        seed_locations[seed] = next_value or current_value
        locations.append(next_value)
        print("=" * 80)
    print(seed_locations)
    print("=" * 80)
    return min(locations)


def part2(filename: str = INPUT_FILE):
    seeds, seed_maps = parse_file(filename)
    seed_ranges = ((seeds[x], seeds[x] + seeds[x + 1]) for x in range(0, len(seeds), 2))

    seed_locations = {}
    for seed_range in seed_ranges:
        print("Seed Range: ", seed_range)
        current_ranges = [seed_range]
        for key in seed_maps.keys():
            next_ranges = []
            while current_ranges:
                seed_range_start, seed_range_end = current_ranges.pop()
                for dest, source, length in seed_maps[key]:
                    overlap_start = max(source, seed_range_start)
                    overlap_end = min(source + length, seed_range_end)
                    if overlap_start < overlap_end:
                        next_ranges.append(
                            (
                                dest + (overlap_start - source),
                                dest + (overlap_end - source),
                            )
                        )
                        if seed_range_start < overlap_start:
                            current_ranges.append((seed_range_start, overlap_start))
                        if seed_range_end > overlap_end:
                            current_ranges.append((overlap_end, seed_range_end))
                        break
                else:
                    next_ranges.append((seed_range_start, seed_range_end))
            print(key, next_ranges)
            current_ranges = [x for x in next_ranges]
        print("=" * 80)
        seed_locations[seed_range] = next_ranges
    return min(min(x) for x in seed_locations.values())[0]


def main():
    print("Advent of Code Day 5")
    input_file = "test.txt"
    if not os.path.exists(input_file):
        get_input_file(day=5)
        if not os.path.exists(input_file):
            return print("Failed to fetch input file.")
    print("=" * 80)
    print(f"Answer Part 1: {part1(input_file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(input_file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
