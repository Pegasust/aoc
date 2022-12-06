#!/usr/bin/env python3

from typing import TextIO


def part1(f: TextIO):
    s = f.read().strip()
    print(f"{s=}")
    for i in range(3, len(s)):
        if len({c for c in s[i-3:i+1]}) == 4:
            return i + 1
    return None

def part2(f: TextIO):
    s = f.read().strip()
    print(f"{s=}")
    for i in range(13, len(s)):
        if len({c for c in s[i-13:i+1]}) == 14:
            return i + 1
    return None

def main(fileloc: str):
    with open(fileloc, "r") as f:
        print(f"{part1(f)=}")

    with open(fileloc, "r") as f:
        print(f"{part2(f)=}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1])

