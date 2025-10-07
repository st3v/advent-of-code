from sys import argv
from math import floor


def getMidElem(elems: list[int]) -> int:
    return elems[floor(len(elems) / 2)]


def order(update: list[int], rules: dict[int, set[int]]) -> tuple[list[int], bool]:
    pos = {p: i for i, p in enumerate(update)}
    reordered = False

    j = 0
    while j < len(update):
        for prereq in rules.get(update[j], []):
            if prereq not in pos:
                continue

            page = update[j]
            prereqPos = pos[prereq]
            if prereqPos > j:
                update[prereqPos], update[j] = update[j], prereq
                pos[prereq], pos[page] = j, prereqPos
                reordered = True
                j -= 1  # reevaluate current position
                break

        j += 1

    return (update, reordered)


total = 0
rules: dict[int, set[int]] = dict()
with open(argv[1], "r") as file:
    for line in file:
        line = line.strip()

        if (rule := line.split("|")) and len(rule) == 2:
            (prereq, page) = map(int, rule)

            if page not in rules:
                rules[page] = set()

            rules[page].add(prereq)
        elif (pages := line.split(",")) and len(pages) > 1:
            update = list(map(int, pages))
            update, reordered = order(update, rules)
            if reordered:
                total += getMidElem(update)

print(total)
