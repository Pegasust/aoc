#!/usr/bin/env python3
import sys
from typing import Iterable

def add_nd(lhs: Iterable[int], rhs: Iterable[int]):
    # Add two generic n-d vector together
    return tuple(l + r for l, r in zip(lhs, rhs))
def negate_nd(vec: Iterable[int]):
    # Negates a generic n-d vector
    return tuple(-e for e in vec)
def norm_infk_nd(vec: Iterable[int]):
    # Mathematical concept where I get the length of the longest vector component
    return max(abs(e) for e in vec)
def sign(e: int):
    return 0 if e == 0 else (1 if e > 0 else -1)

def dir_to_offset(dir: str):
    match dir:
        case "U":
            return (0, 1)
        case "D":
            return (0, -1)
        case "L":
            return (-1, 0)
        case "R":
            return (1, 0)
        case d:
            raise RuntimeError(f"Unknown direction {d}")

def move_knot(knot: list[tuple[int, int]], offset: Iterable[int]):
    knot.append(add_nd(knot[-1], offset))
    return knot

def part1(commands: list[tuple[str, int]]):
    tail_locs: list[tuple[int, int]] = [(0,0)] # keeps track of where tail moved
    # NOTE: I don't need to keep track of head's history here. This is only
    # for ease of debugging
    head_locs : list[tuple[int, int]] = [(0,0)] # keeps track of where head moved
    for dir, rep in commands:
        for _ in range(rep):
            move_knot(head_locs, dir_to_offset(dir))
            offset = add_nd(head_locs[-1], negate_nd(tail_locs[-1]))
            # print(f"{offset=}")
            if norm_infk_nd(offset) <= 1:
                continue # no need to catch up
            move_knot(tail_locs, (sign(e) for e in offset))
    # print(f"{tail_locs=}")
    # print(f"{head_locs=}")
    return len(set(tail_locs))

def part2(commands: list[tuple[str, int]]):
    KNOTS = 10
    # NOTE: I don't need to keep track of any history but tail's. This is only
    # for ease of debugging
    locs = [[(0,0)] for _ in range(KNOTS)] # 10 knots :)
    for dir, rep in commands:
        for _ in range(rep):
            move_knot(locs[0], dir_to_offset(dir)) # move head
            for i in range(1, KNOTS):
                offset = add_nd(locs[i-1][-1], negate_nd(locs[i][-1]))
                if norm_infk_nd(offset) <= 1:
                    continue # no need to catch up
                move_knot(locs[i], (sign(e) for e in offset))
    return len(set(locs[-1]))



def main(lines: Iterable[str]):
    splited = (line.strip().split() for line in lines)
    # -> ["   D 4    ",...] -> [["D", "4"], ...]
    ## Filters out any line that has empty newline and turn repitions into int
    commands = [(comp[0], int(comp[1])) for comp in splited if len(comp) > 0]
    # -> [[], ["D", "4"], ...] -> [["D", 4]]
    print("part1", part1(commands))
    print("part2", part2(commands))
    pass

if __name__=="__main__":
    with open(sys.argv[1], "r") as f:
        main(f)

