"""
https://adventofcode.com/2022/day/1
"""

from typing import Iterable

def calories_sum(input_lines: Iterable[str])->Iterable[int]:
    # idk why this doesn't work with file inputs
    # string parsing is a bit tough here
    elves = [[]]
    for raw_line in input_lines:
        line = raw_line.strip()
        if len(line) == 0:
            elves.append([])
            continue
        elves[-1].append(int(line))
    return (sum(carry) for carry in elves if len(carry) > 0)

def batch_and_exec(input_lines: Iterable[str])->int:
    return sorted(calories_sum(input_lines), reverse=True)[0]

def top3_sum(input_lines: Iterable[str])->int:
    return sum(sorted(calories_sum(input_lines), reverse=True)[:3])


if __name__ ==  "__main__":
    input_f = "2022/d1_input.txt"
    # First elf: [1000, 2000, 3000] -> 6000 calories
    # Second elf: [4000]
    # Third elf: [5000, 6000] -> 11000 calories
    # Fourth elf: [7000, 8000, 9000] -> 24000 calories
    # Fifth elf: [10000]
    # Want to know: which elf is carrying the most calories
    # in this case: 24000
    input = """
    1000
    2000
    3000

    4000

    5000
    6000

    7000
    8000
    9000

    10000
    """
    output = batch_and_exec(input.splitlines())
    assert output == 24000, f"Got {output}, expected {24000}"
    ex_top3 = top3_sum(input.splitlines())
    assert ex_top3 == 45000, f"Got {ex_top3}, expected {45000}"

    with open(input_f) as inp:
        print(batch_and_exec(inp))

    with open(input_f) as inp:
        print(top3_sum(inp))


