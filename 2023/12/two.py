from sys import argv


def unfold(have, want):
    return "?".join([have] * 5), want * 5


def count_arrangements(have, want, current, memo):
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
                return count_arrangements(have[1:], want[1:], 0, memo)
            else:
                return 0
        else:
            return count_arrangements(have[1:], want, 0, memo)
    elif have[0] == "#":
        return count_arrangements(have[1:], want, current + 1, memo)

    key = (have, tuple(want), current)
    if key in memo:
        return memo[key]

    total = count_arrangements(have[1:], want, current + 1, memo)
    total += count_arrangements("." + have[1:], want, current, memo)
    memo[key] = total

    return total


total = 0
with open(argv[1]) as file:
    for line in file:
        have, want = line.strip().split()
        have, want = have.strip(), list(map(int, want.strip().split(",")))
        have, want = unfold(have, want)
        total += count_arrangements(have, want, 0, {})
print(total)
