#!/usr/bin/env python3

def main(file_loc: str):
    with open(file_loc, "r") as f:
        count = 0
        for _line in f:
            line = _line.strip()
            if len(line) == 0:
                continue
            partners = [[int(time) for time in part.split("-")]for part in line.split(",")]
            # check if one range contains the other
            for i in range(2):
                start_l, end_l = partners[i]
                start_r, end_r = partners[1-i]
                if start_l >= start_r and end_l <= end_r:
                    count += 1
                    break


        print("part 1:", count)

    with open(file_loc, "r") as f:
        count = 0
        for _line in f:
            line = _line.strip()
            if len(line) == 0:
                continue
            partners = [[int(time) for time in part.split("-")]for part in line.split(",")]
            # check if overlap at all
            # basically just check the begin and end of one
            start_l, end_l = partners[0]
            start_r, end_r = partners[1]
            should_add = any(
                    any(time in range(partners[1-i][0], partners[1-i][1]+1) 
                for time in partners[i]) for i in range(2))
            count += 1 if should_add else 0
        print("part 2:", count)
            


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise RuntimeError("expected the first argument to point to data file location")
    FILE_LOC=sys.argv[1]
    main(FILE_LOC)

