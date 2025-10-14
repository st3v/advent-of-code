from sys import argv


def count_arrangements(have, want, current):
    if not have:
        if len(want) == 1 and want[0] == current:
            return 1
        elif len(want) == 0:
            return 1
        else:
            return 0

    if not want:
        return 1 if "#" not in have else 0

    if want[0] < current:
        return 0

    if have[0] == ".":
        if current > 0:
            if current == want[0]:
                return count_arrangements(have[1:], want[1:], 0)
            else:
                return 0
        else:
            return count_arrangements(have[1:], want, 0)
    elif have[0] == "#":
        return count_arrangements(have[1:], want, current + 1)

    total = count_arrangements(have[1:], want, current + 1)
    total += count_arrangements("." + have[1:], want, current)
    return total


total = 0
with open(argv[1]) as file:
    for line in file:
        have, want = line.strip().split()
        total += count_arrangements(
            have.strip(), list(map(int, want.strip().split(","))), 0
        )

print(total)
