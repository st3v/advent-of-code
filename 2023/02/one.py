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


def is_valid(counts, limits):
    for color, count in counts.items():
        if count > limits[color]:
            return False
    return True


limits = {"red": 12, "green": 13, "blue": 14}
games = read(argv[1])
total = sum(id for id, counts in games.items() if is_valid(counts, limits))
print(total)
