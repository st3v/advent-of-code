from sys import argv
import re
from collections import defaultdict
from tqdm import tqdm


def read(path):
    with open(path) as file:
        parts = file.read().strip().split("\n\n")

    seed_ranges = []
    mappings = defaultdict(dict)
    for p in parts:
        key, data = p.strip().split(":")
        if key == "seeds":
            nums = [int(s.strip()) for s in data.split()]
            seed_ranges = [(nums[i], nums[i + 1]) for i in range(0, len(nums) - 1, 2)]
        else:
            src, dst = re.findall("([a-z]+)\\-to\\-([a-z]+).*", key)[0]
            ranges = []
            for line in [s for s in data.split("\n") if len(s) > 0]:
                ranges.append(list(map(int, line.strip().split())))
            mappings[src][dst] = ranges
    return seed_ranges, mappings


def map_value(value, src, mappings):
    while src in mappings:
        for dst, ranges in mappings[src].items():
            for dst_start, src_start, range_len in ranges:
                if src_start <= value < src_start + range_len:
                    value = dst_start + (value - src_start)
                    break
            src = dst
            break
    return value


def in_range(value, ranges):
    for start, length in ranges:
        if start <= value < start + length:
            return True
    return False


seed_ranges, mappings = read(argv[1])

inverse_mappings = {
    dst: {src: [[range[1], range[0], range[2]] for range in mappings[src][dst]]}
    for src in mappings
    for dst in mappings[src]
}

min_location = 0
while not in_range(map_value(min_location, "location", inverse_mappings), seed_ranges):
    min_location += 1

print(min_location)
