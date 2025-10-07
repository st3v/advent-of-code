from sys import argv
from collections import defaultdict


def read(path):
    keys, locks = [], []
    with open(path) as file:
        parts = file.read().strip().split("\n\n")

    for p in parts:
        rows = list(map(list, p.split("\n")))
        cols = zip(*rows)
        res = []
        for col in cols:
            res.append(sum(int(c == "#") for c in col))

        is_key = rows[0] == ["."] * 5
        if is_key:
            keys.append(res)
        else:
            locks.append(res)

    return locks, keys


def fit(lock, key):
    for pos in range(5):
        if lock[pos] + key[pos] > 7:
            return False
    return True


def match(locks, keys):
    res = defaultdict(list)
    for l in locks:
        for k in keys:
            if fit(l, k):
                res[tuple(l)].append(k)
    return res


locks, keys = read(argv[1])
matching = match(locks, keys)

total = 0
for lock, keys in matching.items():
    total += len(keys)

print(total)
