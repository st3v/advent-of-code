from sys import argv
from re import findall
from collections import defaultdict
import itertools
from typing import Callable


def groups(data: list[list[str]], func: Callable[[int, int], int]) -> list[list[str]]:
    grouping: dict[int, list[str]] = defaultdict(list)
    for y in range(len(data)):
        for x in range(len(data[y])):
            grouping[func(x, y)].append(data[y][x])
    return list(x for x in map(grouping.get, sorted(grouping)) if x is not None)


def count(line: list[str], word: str) -> int:
    if len(line) < len(word):
        return 0

    s = "".join(line)

    return len(findall(word, s)) + len(findall(word[::-1], s))


matrix: list[list[str]] = []
with open(argv[1], "r") as file:
    for line in file.readlines():
        matrix.append(list(line.strip()))

rows = groups(matrix, lambda x, y: y)
cols = groups(matrix, lambda x, y: x)
fdiag = groups(matrix, lambda x, y: x + y)
bdiag = groups(matrix, lambda x, y: x - y)

total = 0
for line in itertools.chain(rows, cols, fdiag, bdiag):
    total += count(line, "XMAS")

print(total)
