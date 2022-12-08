#!/usr/bin/env python3
import sys
from typing import Iterable
from functools import reduce

def check(grid: list[str], x: int, y: int, memo = None):
    height = int(grid[y][x])
    # print(f"{x=}, {y=}, {height=}")
    top = max((int(grid[_y][x]) for _y in range(0, y)), default=-1)
    bot = max((int(grid[_y][x]) for _y in range(y+1, len(grid))), default=-1)
    left = max(((int(grid[y][_x]) for _x in range(0, x))), default=-1)
    right = max(((int(grid[y][_x]) for _x in range(x+1, len(grid[0])))), default=-1)

    # print(f"max: {[top,bot,left,right]}")
    visible = any(height > max_view for max_view in [top, bot, left, right])
    # print(visible)
    return visible
    
def scene_score(grid: list[str], x: int, y: int, memo = None):
    dirs = [
        ((_y, x) for _y in reversed(range(0, y))), # TOP
        ((_y, x) for _y in range(y+1, len(grid))), # BOT
        ((y, _x) for _x in reversed(range(0, x))), # LEFT
        ((y, _x) for _x in range(x+1, len(grid[0]))), # RIGHT
    ]
    my_height = int(grid[y][x])
    def raytrace(gen):
        counter = 0
        trace = True
        __y, __x = y, x
        for (_y, _x) in gen:
            if not trace:
                break
            __y, __x = _y, _x
            h = int(grid[_y][_x])
            trace = my_height > h
            counter += 1 
        return (counter, __x, __y)

    print(f"{x=}, {y=}, {my_height=}")
    scores = [raytrace(dir) for dir in dirs]
    print(f"{scores=}")
    score = reduce(lambda acc, v: acc * v[0], scores, 1)
    # print(f"{score=}")
    return (score, scores)

def main(lines: Iterable[str]):
    grid = [line.strip() for line in lines if len(line.strip()) > 0]
    memo = None
    print("grid:")
    print("\n".join(grid))
    Y_MAX, X_MAX = len(grid), len(grid[0])
    print(f"{Y_MAX=}, {X_MAX=}")
    part1= sum([check(grid, x, y, memo) for y in range(0, len(grid)-0) for x in range(0, len(grid[0]) -0)])
    print("part1", part1)
    memo2=None
    part2 = max([scene_score(grid, x, y, memo2) for y in range(1, len(grid)-1) for x in range(1,len(grid[0])-1)])
    print("part2", part2)


if __name__=="__main__":
    with open(sys.argv[1], "r") as f:
        main(f)
