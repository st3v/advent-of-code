from sys import argv

total = 0
with open(argv[1]) as file:
    for line in file:
        _, nums = line.strip().split(":")

        want, got = nums.strip().split("|")

        win = set()
        for w in want.strip().split():
            win.add(w.strip())

        matches = 0
        for g in got.strip().split():
            if g.strip() in win:
                matches += 1

        if matches > 0:
            total += 2 ** (matches - 1)

print(total)
