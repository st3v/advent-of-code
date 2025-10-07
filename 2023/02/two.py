from sys import argv
from collections import defaultdict


def read(path):
    games = {}
    with open(path) as file:
        for line in file:
            game, sets = line.strip().split(":")
            id = int(game.split()[1].strip())

            counts = defaultdict(int)
            for s in sets.strip().split(";"):
                for cube in s.split(","):
                    count, color = cube.split()
                    count, color = int(count.strip()), color.strip()
                    if count > counts[color]:
                        counts[color] = count
            games[id] = counts

    return games


def power(counts):
    res = 1
    for count in counts.values():
        res *= count
    return res


games = read(argv[1])
total = sum(power(counts) for counts in games.values())
print(total)
