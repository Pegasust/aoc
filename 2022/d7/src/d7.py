#!/usr/bin/env python3
from typing import Iterable, Optional
from dataclasses import dataclass
from functools import reduce

@dataclass
class File:
    name: str
    is_dir: bool
    children: dict[str, "File"]
    parent: Optional["File"]
    size: Optional[int]

class Main:
    def __init__(self, lines: Iterable[str]):
        self.root = File("/",True, {}, None, None)
        self.cwd = self.root
        self.lines = lines

    def handle_cmd(self, cmdlets: list[str]):
        match cmdlets[0]:
            case "cd":
                dest = cmdlets[1]
                match dest:
                    case "/":
                        self.cwd = self.root
                    case "..":
                        if not self.cwd.parent:
                            return self
                        self.cwd = self.cwd.parent
                    case _:
                        self.cwd = self.cwd.children[dest]
                # validate cwd
                return self
            case "ls":
                return self
            case _:
                raise RuntimeError(f"Unknown command: {cmdlets[0]}")

    def parse(self):
        for _line in self.lines:
            line = _line.strip()
            if len(line) == 0:
                continue
            # print("line:", line)
            if line[0] == "$": # command
                cmdlets = line[1:].split()
                self.handle_cmd(cmdlets)
                continue
            # it's just ls listing, update it to our object storage
            (sz, rel_path) = line.split()
            self.cwd.children[rel_path] = File(name=rel_path, 
                                               is_dir=sz == "dir",
                                               children={}, 
                                               parent=self.cwd, 
                                               size=int(sz) if sz != "dir" else None)
        return self

    def solve(self):
        self.parse()
        def sized(file: File, parent: Optional[File]):
            """
            alternative file
            """
            if file.size:
                return file
            retval = File(file.name, file.is_dir, {}, None, None)
            children = {rel_path: sized(f, retval) for rel_path, f in file.children.items()}
            retval.children = children
            retval.parent = parent
            retval.size = sum(c.size for c in children.values())
            return retval

        def sum_with_threshold(sized_file: File, max_sz: int) -> int:
            assert sized_file.size is not None
            sz = 0
            if sized_file.size <= max_sz and len(sized_file.children) != 0:
                # print("qual:", sized_file.name)
                sz = sized_file.size
            return sum(sum_with_threshold(c, max_sz) for c in sized_file.children.values()) + sz
        sized_root = sized(self.root, None)

        part1 = sum_with_threshold(sized_root, 100_000)
        print("part1", part1)

        def directories(file: File) -> list[File]:
            if not file.is_dir:
                return []
            return [file] + [dir for f in file.children.values() for dir in directories(f)]

        def upper_bound(sized_file: File, min_sz: int) -> list[File]:
            assert sized_file.size is not None
            if sized_file.size < min_sz or len(sized_file.children) == 0: 
                return []
            min_f: File = sized_file
            contests = [c for e in sized_file.children.values() for c in upper_bound(e, min_sz)]
            return [min_f] + contests

        TOTAL=70_000_000
        NEED=30_000_000
        assert sized_root.size is not None
        DELETE=NEED-(TOTAL-sized_root.size)
        print(f"{DELETE=}")
        part2 = upper_bound(sized_root, DELETE)
        p = sorted(part2, key=lambda x: x.size or 0)
        # print("part2 qual:", "\n".join([f"({e.name}, {e.size})" for e in p]))
        print("part2", p[0].size if part2 else "None")

        sorted_dirs = sorted(directories(sized_root), key=lambda x: x.size or 0)
        # Before is_dir: 176 for part 2
        print(f"directories ({len(sorted_dirs)}):")
        print("\n".join(f"{dir.name}\t{dir.size}" for dir in sorted_dirs))


def main(lines: Iterable[str]):
    Main(list(lines)).solve()



if __name__ == "__main__":
    import sys
    with open(sys.argv[1], "r") as f:
        main(f)
