from sys import argv
from collections import defaultdict

path = argv[1]
iterations = int(argv[2])

with open(path, "r") as file:
    stones = list(map(int, file.read().strip().split()))


stone_counts: dict[int, int] = defaultdict(int)
for stone in stones:
    stone_counts[stone] += 1

for _ in range(iterations):
    new_counts: dict[int, int] = defaultdict(int)

    for stone_value, count in stone_counts.items():
        if stone_value == 0:
            new_counts[1] += count
        elif len(str(stone_value)) % 2 == 0:
            s = str(stone_value)
            mid = len(s) // 2
            left = int(s[:mid])
            right = int(s[mid:])
            new_counts[left] += count
            new_counts[right] += count
        else:
            new_value = stone_value * 2024
            new_counts[new_value] += count

    stone_counts = new_counts

total = sum(stone_counts.values())
print(total)
