from sys import argv


def num_matches(want, have):
    want = set(want)
    return sum(1 for h in have if h in want)


def read(path):
    matches = []
    with open(path) as file:
        for line in file:
            _, nums = line.strip().split(":")

            want, have = nums.strip().split("|")
            matches.append(
                num_matches(
                    [w.strip() for w in want.strip().split()],
                    [h.strip() for h in have.strip().split()],
                )
            )
    return matches


def add_copies(i, matches, copies):
    for j in range(matches[i]):
        copies[i + j + 1] += copies[i]


matches = read(argv[1])
copies = {i: 1 for i in range(len(matches))}
total = 0
for i, m in enumerate(matches):
    total += copies[i]
    add_copies(i, matches, copies)
print(total)
