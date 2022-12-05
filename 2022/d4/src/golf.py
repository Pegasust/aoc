#!/usr/bin/env python3

FILE_LOC="./data/submission.txt"
print(sum([any(g[t][0] <= g[1-t][0] and g[1-t][1] <= g[t][1] for t in range(2)) for g in ([[int(t) for t in w.split("-")] for w in l.split(",")] for l in (l.strip() for l in open(FILE_LOC, "r")) if len(l) > 0)]))
print(sum([any(g[1-t][0] <= g[t][1] and g[t][1] <= g[1-t][1] for t in range(2)) for g in ([[int(t) for t in w.split("-")] for w in l.split(",")] for l in (l.strip() for l in open(FILE_LOC, "r")) if len(l) > 0)]))
