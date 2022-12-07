#!/usr/bin/env python3
from typing import Iterable


def main(lines: Iterable[str]):
    ROOT_WD = [""]
    ROOT="/".join(ROOT_WD)
    cwd = ROOT_WD
    dirs = {ROOT: 0}
    for command in filter(lambda line: len(line) > 0, map(lambda line: line.strip(), lines)):
        match command.split():
            case ["$", "cd", "/"]:
                cwd = ROOT_WD
            case ["$", "cd", ".."]:
                if len(cwd) > 1:
                    cwd.pop()
            case ["$", "cd", rel_path]:
                cwd.append(rel_path)
            case ["$", "ls"]:
                pass
            case ["dir", rel_path]:
                dirs["/".join(cwd + [rel_path])] = 0
            case [dir_sz, _]:
                for i in range(len(cwd)):
                    dirs["/".join(cwd[:i+1])] += int(dir_sz)
            case spl:
                raise RuntimeError(f"Unexpected entry: {spl}")
    # sorted_dir = sorted(dirs.items(), key=lambda v: v[1])
    # print(f"directories ({len(sorted_dir)})")
    # print("\n".join(f"{dir}\t{sz}" for dir, sz in sorted_dir))
    print("part 1:", sum(dir_sz for dir_sz in dirs.values() if dir_sz <= 100_000))
    TOTAL=70_000_000
    NEED=30_000_000
    DELETE=NEED - (TOTAL - dirs[ROOT])
    part2 = min(((dir, sz) for dir,sz in dirs.items() if sz >= DELETE), key=lambda v: v[1])
    print("part 2:", part2)

if __name__ == "__main__":
    import sys
    with open(sys.argv[1], "r") as f:
        main(f)

"/".join([""])
