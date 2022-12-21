#!/usr/bin/env python3
import sys
from typing import Iterable
import os

def part1(insns: list[list[str]], init = 1):
    reg = init
    regs = [reg]
    for insn in insns:
        match insn:
            case ["noop"]:
                regs.append(regs[-1])
            case ["addx", adder]:
                reg += int(adder)
                regs.append(regs[-1])
                regs.append(reg)
            case e:
                raise RuntimeError(f"lol what case is this? {e=}")
    print("regs", os.pathsep.join(str(reg) for reg in regs))

    def ret(queries: Iterable[int]):
        signal_bases = [(i, regs[i-1]) for i in queries]
        print(signal_bases)
        return sum(signal[0] * signal[1] for signal in signal_bases)
    return (regs, ret)

def part2(insns: list[list[str]], init = 1, width = 40):
    regs, _ = part1(insns, init)
    position = lambda cycle: (cycle) % width
    active = [['#' if (position(cycle) in range(regs[cycle]-1, regs[cycle]+2)) else '.'
        for cycle in range(row, min(row + width, len(regs)))] 
        for row in range(0, len(regs),width)]
    return active

def main(lines: Iterable[str]):
    instructions = [s.split() for s in (line.strip() for line in lines) if len(s) > 0]
    # print("part1", part1(instructions)([1,2,3,4,5]))
    print("part1", part1(instructions)[1]([20, 60, 100, 140, 180, 220]))
    part2_ans = part2(instructions)
    print("part2")
    for line in part2_ans:
        print(str().join(line))
    pass


def _main(filename: str):
    with open(filename, "r") as f:
        main(f)

if __name__=="__main__":
    _main(sys.argv[1])

# For neovim integrated repl which can evaluate per selection
REPL = """
_main("./data/example.txt")
_main("./data/submission.txt")
main([
    "noop",
    "addx 3",
    "addx -5"
])

[1, 1, 1, 4, 4, -1, -1, -6, -6]

"""
