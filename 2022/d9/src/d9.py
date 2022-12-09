#!/usr/bin/env python3
import sys
from typing import Iterable, Generator
from functools import reduce
from itertools import product

def add_nd(lhs: Iterable[int], rhs: Iterable[int]):
    return tuple(l + r for l, r in zip(lhs, rhs))
def negate_nd(vec: Iterable[int]):
    return tuple(-e for e in vec)
def norm_1k_nd(vec: Iterable[int]):
    return sum(abs(e) for e in vec)
def norm_infk_nd(vec: Iterable[int]):
    return max(abs(e) for e in vec)


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
def sign(e: int):
    return 0 if e == 0 else (1 if e > 0 else -1)

def move_knot(knot: list[tuple[int, int]], offset: Iterable[int]):
    knot.append(add_nd(knot[-1], offset))
    return knot

def part1(commands: list[tuple[str, int]]):
    tail_locs: list[tuple[int, int]] = [(0,0)] # keeps track of where tail moved
    head_locs : list[tuple[int, int]] = [(0,0)] # keeps track of where head moved
    for dir, rep in commands:
        for _ in range(rep):
            move_knot(head_locs, dir_to_offset(dir))
            offset = add_nd(head_locs[-1], negate_nd(tail_locs[-1]))
            # print(f"{offset=}")
            match norm_1k_nd(offset), norm_infk_nd(offset):
                case (0, _) | (1, _) | (2, 1):
                    pass # don't need to catchup
                case (_, _):
                    # negate & normalize in inf_k
                    move_knot(tail_locs, (sign(e) for e in offset))
                case e:
                    raise RuntimeError(f"Unknown case {e}\n{tail_locs=}\n{head_locs=}")
    # print(f"{tail_locs=}")
    # print(f"{head_locs=}")

    return len(set(tail_locs))

def part2(commands: list[tuple[str, int]]):
    KNOTS = 10
    locs = [[(0,0)] for _ in range(KNOTS)] # 10 knots :)
    for dir, rep in commands:
        for _ in range(rep):
            move_knot(locs[0], dir_to_offset(dir)) # move head
            for i in range(1, KNOTS):
                offset = add_nd(locs[i-1][-1], negate_nd(locs[i][-1]))
                match norm_1k_nd(offset), norm_infk_nd(offset):
                    case (0, _) | (1, _) | (2, 1):
                        pass # don't need to catchup
                    case (_, _):
                        # negate & normalize in inf_k
                        move_knot(locs[i], (sign(e) for e in offset))
                    case e:
                        raise RuntimeError(f"Unknown case {e}\n{locs[i]=}\n{locs[i-1]=}")
    return len(set(locs[-1]))



def main(lines: Iterable[str]):
    splited = (line.strip().split() for line in lines)
    striped_lines = [(comp[0], int(comp[1])) for comp in splited if len(comp) > 0]
    # print(striped_lines)
    commands = [(comp[0], int(comp[1])) for comp in striped_lines]
    print("part1", part1(commands))
    print("part2", part2(commands))
    pass

if __name__=="__main__":
    with open(sys.argv[1], "r") as f:
        main(f)
