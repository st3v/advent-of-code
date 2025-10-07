from sys import argv
from math import floor


def getMidElem(elems: list[int]) -> int:
    return elems[floor(len(elems) / 2)]


def isOrdered(update: list[int], rules: dict[int, set[int]]) -> bool:
    present = set(update)
    seen: set[int] = set()
    for page in update:
        if page in rules:
            for prereq in rules[page]:
                if prereq in present and prereq not in seen:
                    return False

        seen.add(page)

    return True


rules: dict[int, set[int]] = dict()
with open(argv[1], "r") as file:
    for line in file:
        line = line.strip()
        if line == "":
            break

        (prereq, page) = map(int, line.split("|"))

        if page not in rules:
            rules[page] = set()

        rules[page].add(prereq)

    total = 0
    for line in file:
        update = list(map(int, line.strip().split(",")))
        if isOrdered(update, rules):
            total += getMidElem(update)

print(total)
