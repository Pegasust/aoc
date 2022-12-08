#!/usr/bin/env python3
import sys
from typing import Iterable, Generator
from functools import reduce
from itertools import product
def dirs(grid: list[str], x: int, y: int) -> list[Generator[tuple[int, int], None, None]]:
    return [
        ((_y, x) for _y in reversed(range(0, y))), # TOP
        ((_y, x) for _y in range(y+1, len(grid))), # BOT
        ((y, _x) for _x in reversed(range(0, x))), # LEFT
        ((y, _x) for _x in range(x+1, len(grid[0]))), # RIGHT
    ] # my IDE, py-lsp is very bad at retaining Generator, idk why

def part_1(grid: list[str], x: int, y: int):
    height = int(grid[y][x])
    return any(height > max((int(grid[_y][_x]) for _y, _x in gen), default=-1) for gen in dirs(grid, x, y))
    
def scene_score(grid: list[str], x: int, y: int):
    _dirs = dirs(grid, x, y)
    my_height = int(grid[y][x])
    def raytrace(gen):
        counter = 0
        for (_y, _x) in gen:
            counter += 1 
            if my_height <= int(grid[_y][_x]):
                break
        return counter
    return reduce(lambda acc, v: acc * v, map(raytrace, _dirs))

def main(lines: Iterable[str]):
    grid = [line.strip() for line in lines if len(line.strip()) > 0] # strip traling newlines
    Y_MAX, X_MAX = len(grid), len(grid[0])
    part1 = sum(part_1(grid, x, y) for x, y in product(range(X_MAX), range(Y_MAX)))
    part2 = max(scene_score(grid, x, y) for x, y in product(range(1, X_MAX-1), range(1, Y_MAX-1)))
    print(f"{part1=}, {part2=}")

if __name__=="__main__":
    with open(sys.argv[1], "r") as f:
        main(f)
