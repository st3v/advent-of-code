from sys import argv

grid = []
with open(argv[1]) as file:
    for line in file:
        grid.append(list(line.strip()))

transposed = list(map(list, zip(*grid)))
total = 0
for col in transposed:
    stones = 0
    for i in range(len(col) - 1, -1, -1):
        if col[i] == "O":
            stones += 1
        elif col[i] == "#":
            for j in range(stones):
                total += len(col) - i - 1 - j
            stones = 0
    for j in range(stones):
        total += len(col) - j

print(total)
