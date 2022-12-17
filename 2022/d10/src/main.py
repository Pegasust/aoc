#!/usr/bin/env python3
import sys
from typing import Iterable, Optional
from dataclasses import dataclass
import os
import string
from functools import reduce

@dataclass
class RectBound:
    bot_left: tuple[int, int]
    top_right: tuple[int, int]

@dataclass
class Sensor:
    loc: tuple[int, int]
    radius_1k: int
    nearest_beacon: tuple[int, int]
    _rect_bound: Optional[RectBound] = None # inclusive
    
    def rect_bound(self):
        if not self._rect_bound:
            self._rect_bound = RectBound(\
                (self.loc[0]-self.radius_1k, self.loc[1]-self.radius_1k), 
                (self.loc[0]+self.radius_1k, self.loc[1]+self.radius_1k), 
            )
        return self._rect_bound

def vec2d_str(x: str, y: str):
    return (int(x), int(y))

def vec_diff(lhs: Iterable[int], rhs: Iterable[int]):
    return tuple(l - r for l, r in zip(lhs, rhs))

def norm_1k(vec: Iterable[int]):
    return sum(abs(e) for e in vec)

@dataclass
class SolutionBound:
    min_x: int
    min_y: int
    max_x: int
    max_y: int

def solution_bound(sensors: list[Sensor]):
    return SolutionBound(min(sensor.loc[0] - sensor.radius_1k for sensor in sensors), 
                         min(sensor.loc[1] - sensor.radius_1k for sensor in sensors),
                         max(sensor.loc[0] + sensor.radius_1k for sensor in sensors), 
                         max(sensor.loc[1] + sensor.radius_1k for sensor in sensors),
                         )

def which_sensor(loc: tuple[int, int], sensors: list[Sensor]):
    """
    Arbitrary sensor number, not nearest or anything. 
    Actually, this fancies the lower index
    """
    for i, sensor in enumerate(sensors):
        if norm_1k(vec_diff(sensor.loc, loc)) <= sensor.radius_1k:
            return (i, sensor if sensor.loc == loc else None)
    return None

def beacons_set(sensors: list[Sensor]):
    return set(sensor.nearest_beacon for sensor in sensors)

def gen_graph(sensors: list[Sensor], sol_bound: Optional[SolutionBound] = None):
    sol_bound = sol_bound if sol_bound is not None else solution_bound(sensors)
    beacons = beacons_set(sensors)
    return [[which_sensor((x, y), sensors) if (x, y) not in beacons else 'B'
        for x in range(sol_bound.min_x, sol_bound.max_x + 1)] 
        for y in range(sol_bound.min_y, sol_bound.max_y + 1)]

def render_graph(graph: list[list[None | tuple[int, Optional[Sensor]] | str]]):
    def sensor_display(x: None | tuple[int, Optional[Sensor]] | str):
        match x:
            case (int(v), s):
                sensor = ("0123456789"+string.ascii_lowercase)
                signal = (")!@#$%^&*("+string.ascii_uppercase)
                return (signal if s is not None else sensor)[v]
            case None:
                return '.'
            case str(s):
                return s
            case e:
                raise RuntimeError(f"Unexpected {e}")

    return list(" ".join(sensor_display(e) if e else '.' for e in row) for row in graph)

def sensor_range_at(sensor: Sensor, y: int):
    effective_radius = max(sensor.radius_1k - abs(y - sensor.loc[1]), 0)
    if effective_radius == 0 and sensor.loc[1] != y:
        return iter([])
    return range(sensor.loc[0] - effective_radius, sensor.loc[0] + effective_radius + 1)

def index_render_graph(rendered_graph: list[str], sol: SolutionBound):
    return os.linesep.join(f"{str(i + sol.min_y).zfill(3)} {row}" 
        for i, row in enumerate(rendered_graph))

def part1(sensors: list[Sensor], y:int):
    sol = solution_bound(sensors)
    print(sol)
    # rendered_graph = render_graph(gen_graph(sensors, sol))
    # print(index_render_graph(rendered_graph, sol))
    beacons = beacons_set(sensors)
    ranges = list(set(sensor_range_at(sensor, y))
        for sensor in sensors)
    print("ranges", ranges)
    x_sense = reduce(lambda lhs, rhs: lhs.union(rhs), ranges).difference({beacon[0] for beacon in beacons if beacon[1] == y})
    # return sum((x, y) not in beacons and which_sensor((x, y), sensors) is not None
    #     for x in range(sol.min_x, sol.max_x + 1))
    print("x_sense", x_sense)
    return len(x_sense)

def part2(sensors: list[Sensor], y:int):
    pass


def sensor_from_input_line(line: str):
    # print(line)
    spl = line.split("=")
    # print(spl)
    _, sensor_x, sensor_y, beacon_x, beacon_y =spl 
    digit_only = lambda x: "".join(filter(lambda v: isinstance(v, str) and v in "0123456789-", x))
    sensor_loc = vec2d_str(digit_only(sensor_x), digit_only(sensor_y))
    beacon_loc = vec2d_str(digit_only(beacon_x), beacon_y)
    return Sensor(sensor_loc, norm_1k(vec_diff(beacon_loc, sensor_loc)), beacon_loc)

def main(lines: Iterable[str]):
    sensors = list(sensor_from_input_line(stripped_line) 
        for stripped_line in (line.strip() for line in lines) if len(stripped_line) > 0)
    beacons = beacons_set(sensors)
    print(os.linesep.join(repr(sensor) for sensor in sensors))
    print("beacons:", beacons)
    y1, y2 = 10, 2000000
    print("part1", part1(sensors, y1), part1(sensors, y2))
    # print("part2", part2(sensors, y1), part2(sensors, y2))
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

"""
