from sys import argv
import re
from collections import defaultdict


def read(path):
    with open(path) as file:
        parts = file.read().strip().split("\n\n")

    seeds = []
    mappings = defaultdict(dict)
    for p in parts:
        key, data = p.strip().split(":")

        if key == "seeds":
            seeds = [int(s.strip()) for s in data.split()]
        else:
            src, dst = re.findall("([a-z]+)\\-to\\-([a-z]+).*", key)[0]
            ranges = []
            for line in [s for s in data.split("\n") if len(s) > 0]:
                ranges.append(list(map(int, line.strip().split())))
            mappings[src][dst] = ranges
    return seeds, mappings


def map_seed(seed, mappings):
    res = seed
    src = "seed"
    while src in mappings:
        for dst, ranges in mappings[src].items():
            for dst_start, src_start, range_len in ranges:
                if src_start <= res < src_start + range_len:
                    res = dst_start + (res - src_start)
                    break
            src = dst
    return res


seeds, mappings = read(argv[1])

min = float("inf")
for s in seeds:
    n = map_seed(s, mappings)
    if n < min:
        min = n
print(min)
