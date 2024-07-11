import math
from typing import Self
from enum import IntEnum
from pathlib import Path
from datetime import date
from http.client import HTTPResponse
from urllib.request import urlopen, Request

KEY_FILE = Path("key.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")
TEST_FILE = Path(__file__).with_name("test2.txt")


def get_input_file(advent_date: date):
    if INPUT_FILE.exists():
        return
    url = f"https://adventofcode.com/{advent_date.year}/day/{advent_date.day}/input"
    req = Request(url)
    req.add_header("Cookie", f"session={KEY_FILE.read_text()}")
    resp: HTTPResponse = urlopen(req)
    INPUT_FILE.write_bytes(resp.read(int(resp.getheader("Content-Length"))))


class Pulse(IntEnum):
    HIGH = 1
    LOW = 0


class Module:
    def __init__(
        self,
        module_name: str,
        module_type: str,
        receivers: list[str],
        senders: list[str],
    ) -> None:
        self.module_name = module_name
        self.module_type = module_type
        self.receivers = receivers
        self.ON = False
        self.senders: dict[str, bool] = {s: Pulse.LOW for s in senders}

    def __repr__(self) -> str:
        return f"Module(module_name={repr(self.module_name)}, module_type={repr(self.module_type)}, receivers={repr(self.receivers)}, senders={repr(self.senders)})"

    def receive(self, pulse: Pulse, sender: Self):
        if self.module_type == "broadcaster":
            return pulse
        elif self.module_type == "%":
            if pulse:
                return
            self.ON = not self.ON
            return Pulse.HIGH if self.ON else Pulse.LOW

        elif self.module_type == "&":
            self.senders[sender.module_name] = pulse
            return Pulse.LOW if all(self.senders.values()) else Pulse.HIGH
        else:
            raise ValueError(f"Invalid Module Type: {self.module_type}")


def parse_data(path: Path):
    data = []
    for line in path.open().readlines():
        name, rest = line.strip().split(" -> ")
        rest = list(map(str.strip, rest.split(",")))
        data.append((name, rest))
    return data


def get_modules(path: Path):
    modules: dict[str, Module] = {}
    data = parse_data(path)
    for item in data:
        name, receivers = item
        if name == "broadcaster":
            modules[name] = Module(name, name, receivers, [])
            continue
        name, type = name[1:], name[0]
        senders = [x if x == "broadcaster" else x[1:] for x, y in data if name in y]
        modules[name] = Module(name, type, receivers, senders)
    return modules


def operate_machine(path: Path, *, button_presses: int | None = None):
    modules = get_modules(path)

    presses = 0
    while True:
        presses += 1
        if button_presses and presses > button_presses:
            break

        emissions = [(modules.get("broadcaster"), Pulse.LOW, None)]
        while emissions:
            receiver, pulse, sender = emissions.pop(0)
            yield pulse, presses, receiver
            if receiver is None:
                continue
            pulse = receiver.receive(pulse, sender)
            if pulse is None:
                continue
            sender = receiver
            emissions += [
                (modules.get(receiver_name), pulse, sender)
                for receiver_name in sender.receivers
            ]


def part1(path: Path):
    high_pulses = low_pulses = 0
    for pulse, *_ in operate_machine(path, button_presses=1000):
        if pulse:
            high_pulses += 1
        else:
            low_pulses += 1
    return high_pulses * low_pulses


def part2(path: Path):
    min_presses: dict[str, int | None] | None = None
    for _, presses, receiver in operate_machine(path):
        if receiver and receiver.module_name == "jz" and any(receiver.senders.values()):
            if min_presses is None:
                min_presses = {k: None for k in receiver.senders.keys()}
            k = next(k for k, v in receiver.senders.items() if v)
            if min_presses[k] is not None:
                continue
            min_presses[k] = presses
            if all(min_presses.values()):
                break
    return math.lcm(*min_presses.values())


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
    main()
