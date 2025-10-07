from sys import argv


def read(path):
    with open(path, "r") as file:
        towels, patterns = file.read().strip().split("\n\n")

    towels = [t.strip() for t in towels.strip().split(",")]
    patterns = [p.strip() for p in patterns.strip().split("\n")]

    return (towels, patterns)


def valid(pattern, towels, seen):
    if pattern in seen:
        return seen[pattern]

    for t in towels:
        l = len(t)
        if l > len(pattern):
            continue

        if l == len(pattern) and pattern == t:
            seen[pattern] = True
            return True

        if pattern[:l] == t and valid(pattern[l:], towels, seen):
            seen[pattern] = True
            return True

    seen[pattern] = False
    return False


towels, patterns = read(argv[1])
towels.sort(key=lambda x: -len(x))

total = 0
for p in patterns:
    if valid(p, towels, {}):
        total += 1

print(total)
