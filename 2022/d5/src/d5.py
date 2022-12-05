#!/usr/bin/env python3
from typing import Literal, Union, Iterable, Optional
from dataclasses import dataclass

@dataclass
class MoveInsn:
    how_many: int
    from_crate: int
    to_crate: int

    @classmethod
    def from_line(cls, line: str):
        tokens = line.strip().split()
        v = map(lambda v: int(tokens[v]), [1, 3, 5]) # indices of "number" token
        return cls(*v) # this is basically calls the constructor

def part1(crates: list[list[str]], insns: list[MoveInsn]) -> str:
    for move in insns:
        for _ in range(move.how_many):
            crates[move.to_crate - 1].append(crates[move.from_crate - 1].pop())
    return "".join([crate[-1] for crate in crates])

def part2(crates: list[list[str]], insns: list[MoveInsn]) -> str:
    for move in insns:
        pops =([crates[move.from_crate - 1].pop() for _ in range(move.how_many)])
        crates[move.to_crate - 1].extend(reversed(pops))
    return "".join([crate[-1] for crate in crates])


def copy_crates(crate_stacks: list[list[str]]):
    return [c[:] for c in crate_stacks]

def main(input_lines: Iterable[str]):
    # Assuming each crate name is single char
    PARSE_CRATE = 0
    PARSE_INSNS = 1

    parse_state = 0
    crates_str = []
    crate_stacks: Optional[list[list[str]]] = None
    moves = []

    for _line in input_lines:
        if len(_line.strip()) == 0:
            # neovim copy-paste doesn't work too well, excuse me
            continue
        match parse_state:
            case 0:
                crates = [s.strip() for s in _line.split()]
                if crates[0] == "1":
                    parse_state = PARSE_INSNS
                    # Begin propagating
                    crate_stacks = [[] for _ in range(len(crates))]
                    for crate_line in reversed(crates_str):
                        crate_decls = [crate_line[i] for i in range(1, len(crate_line), 4)]
                        for crate, stack in zip(crate_decls, crate_stacks):
                            if crate == ' ':
                                continue
                            stack.append(crate)
                    # print(crate_stacks)
                else:
                    crates_str.append(_line)
                pass
            case 1:
                moves.append(MoveInsn.from_line(_line))
                # print(moves)
                pass

    assert crate_stacks is not None, "input must indicate crates input"
    print("part1", part1(copy_crates(crate_stacks), moves))
    print("part2", part2(copy_crates(crate_stacks), moves))
    pass

if __name__ == "__main__":
    import sys
    with open(sys.argv[1], "r") as f:
        main(f)
