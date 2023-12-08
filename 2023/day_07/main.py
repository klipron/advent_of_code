import os
from collections import Counter

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
        for i, line in enumerate(f.readlines()):
            yield (line.strip().split())


class SameHandError(Exception):
    ...


class Hand:
    def __init__(self, cards: str, joker_rules=False) -> None:
        self.cards = cards
        self.joker_rules = joker_rules
        counter = Counter(self.cards)
        if joker_rules:
            if "J" in self.cards:
                joker_value = counter["J"]
                if joker_value < 5:
                    card, _ = max(
                        [
                            (card, count)
                            for card, count in counter.items()
                            if card != "J"
                        ],
                        key=lambda x: x[1],
                    )
                    counter = Counter(self.cards.replace("J", card))
        values = counter.values()
        self.process_cards(values)

    def __repr__(self) -> str:
        return (
            f"Hand(cards='{self.cards}', type='{self.type}', strength={self.strength})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                f"Can't compare {self.__class__} and {other.__class__}"
            )
        return self.strength == other.strength

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                f"Can't compare {self.__class__} and {other.__class__}"
            )
        card_strengths = "AKQJT98765432"[::-1]
        if self.joker_rules:
            card_strengths = "AKQT98765432J"[::-1]
        if self == other:
            if self.cards == other.cards:
                raise SameHandError
            for i in range(len(self.cards)):
                x = card_strengths.find(self.cards[i])
                y = card_strengths.find(other.cards[i])
                if x == y:
                    continue
                return x < y
        return self.strength < other.strength

    def process_cards(self, values):
        if 5 in values:
            self.type = "Five of a kind"
            self.strength = 7
        elif 4 in values:
            self.type = "Four of a kind"
            self.strength = 6
        elif 3 in values and 2 in values:
            self.type = "Full house"
            self.strength = 5
        elif 3 in values:
            self.type = "Three of a kind"
            self.strength = 4
        elif 2 in values and Counter(values)[2] > 1:
            self.type = "Two pair"
            self.strength = 3
        elif 2 in values:
            self.type = "One pair"
            self.strength = 2
        elif max(values) == 1:
            self.type = "High card"
            self.strength = 1


def part1(filename: str):
    hands = sorted(
        ((Hand(cards), int(bid)) for cards, bid in parse_file(filename)),
        key=lambda x: x[0],
    )
    ans = sum(bid * rank for rank, (_, bid) in enumerate(hands, start=1))
    return ans


def part2(filename: str):
    hands = sorted(
        (
            (Hand(cards, joker_rules=True), int(bid))
            for cards, bid in parse_file(filename)
        ),
        key=lambda x: x[0],
    )
    ans = sum(bid * rank for rank, (_, bid) in enumerate(hands, start=1))
    return ans


def main():
    day = 7
    print(f"Advent of Code Day {day}")
    input_file = INPUT_FILE
    if not os.path.exists(input_file):
        get_input_file(day=day)
        if not os.path.exists(input_file):
            return print("Failed to fetch input file.")
    print("=" * 80)
    print(f"Answer Part 1: {part1(input_file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(input_file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
