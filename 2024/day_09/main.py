import os
import ssl
import time
from pathlib import Path
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


def get_disk_map(path: Path):
    fp = path.open()
    while data := fp.read(2):
        block_size, free_space = map(lambda x: int(x.strip() or 0), data)
        yield dict(
            size=block_size, free_space=free_space, allocations=[], reallocated=0
        )


def calculate_checksum(disk_map):
    idx = 0
    total = 0
    for id, block in enumerate(disk_map):
        for _ in range(block["size"]):
            total += id * idx
            idx += 1
        for _ in range(block["reallocated"]):
            idx += 1
        for iid in block["allocations"]:
            total += iid * idx
            idx += 1
        for _ in range(block["free_space"]):
            idx += 1
    return total


def get_disk_map_text(disk_map):
    text = ""
    for id, block in enumerate(disk_map):
        for _ in range(block["size"]):
            text += str(id)
        for _ in range(block["reallocated"]):
            text += "."
        for iid in block["allocations"]:
            text += str(iid)
        for _ in range(block["free_space"]):
            text += "."
    return text


def solve(path: Path, *, test=False):
    disk_map = tuple(get_disk_map(path))
    for idx in range(len(disk_map)):
        print(idx, end="\r")
        if not disk_map[idx]["size"]:
            continue
        while disk_map[idx]["free_space"]:
            for edx in range(len(disk_map) - 1, -1, -1):
                if not disk_map[idx]["free_space"]:
                    break
                if not disk_map[edx]["size"]:
                    continue
                while disk_map[edx]["size"] and disk_map[idx]["free_space"]:
                    disk_map[idx]["allocations"].append(edx)
                    disk_map[idx]["free_space"] -= 1
                    disk_map[edx]["size"] -= 1
    show_answer(part=1, answer=calculate_checksum(disk_map), test=test)

    disk_map = tuple(get_disk_map(path))
    for edx in range(len(disk_map) - 1, -1, -1):
        print(edx, end="\r")
        for idx in range(0, edx):
            if disk_map[idx]["free_space"] < disk_map[edx]["size"]:
                continue
            list.extend(disk_map[idx]["allocations"], [edx] * disk_map[edx]["size"])
            disk_map[idx]["free_space"] -= disk_map[edx]["size"]
            disk_map[edx]["reallocated"] += disk_map[edx]["size"]
            disk_map[edx]["size"] = 0
            break
    show_answer(part=2, answer=calculate_checksum(disk_map), test=test)


def get_input_file(year: int, day: int):
    if INPUT_FILE.exists():
        return
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    req = Request(url)
    req.add_header("Cookie", f"session={os.environ["AOC_SESSION"]}")
    context = ssl._create_unverified_context()
    try:
        resp: HTTPResponse = urlopen(req, context=context)
    except HTTPError as e:
        return print(e.read().decode())
    INPUT_FILE.write_bytes(resp.read(int(resp.getheader("Content-Length"))))


def show_answer(*, part: int, answer: int, test=False):
    print(
        f"{"Test Input " if test else ""}Answer Part {part}: {answer or ''}".ljust(50),
        "=" * 80,
        sep="\n",
    )


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    print(f"Advent of Code {year} Day {day}")
    print("=" * 80)
    get_input_file(year, day)
    if not INPUT_FILE.exists():
        return
    if TEST_FILE.exists():
        solve(TEST_FILE, test=True)
    solve(INPUT_FILE)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
