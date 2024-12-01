import shutil
from datetime import date
from pathlib import Path
from typing import Any, TypeVar, Callable


T = TypeVar("T")


def get_input(prompt: str, validate: Callable[[Any], T | None]) -> T | None:
    while 1:
        value = input(prompt + " or press Enter to cancel: ")
        if not value:
            return print("Script cancelled.")
        value = validate(value)
        if value is None:
            print(", please try again.")
            continue
        return value


def validate_int(value):
    try:
        return int(value)
    except ValueError as e:
        print(e, end="")


def validate_year(year):
    year = validate_int(year)
    if year is None:
        return
    max_year = date.today().year
    if year in range(2015, max_year + 1):
        return year
    print(f"Year must be in range {2015} to {max_year}", end="")


def validate_day(day):
    day = validate_int(day)
    if day is None:
        return
    if day in range(1, 26):
        return day
    print(f"Day must be in range 1 to 26", end="")


def main():
    print("Create Advent of Code Day Directory")
    year = get_input("Enter Year", validate_year)
    if year is None:
        return
    day = get_input("Enter Day", validate_day)
    if day is None:
        return

    path = Path(str(year), f"day_{day:0>2}")
    path.mkdir(exist_ok=True, parents=True)
    file_path = path / "main.py"
    if file_path.exists():
        return print(f"Advent of Code {year} Day {day} '{file_path}' already exists.")
    shutil.copy("sample", file_path)
    print(f"Advent of Code {year} Day {day} '{file_path}' created successfully.")


if __name__ == "__main__":
    main()
