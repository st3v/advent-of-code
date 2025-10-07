from sys import argv

matrix: list[list[str]] = []
with open(argv[1], "r") as file:
    for line in file.readlines():
        matrix.append(list(line.strip()))

matches = ["MAS", "SAM"]
total = 0
for y in range(0, len(matrix) - 2):
    for x in range(0, len(matrix[y]) - 2):
        diag1 = "".join([matrix[y][x], matrix[y + 1][x + 1], matrix[y + 2][x + 2]])
        diag2 = "".join([matrix[y][x + 2], matrix[y + 1][x + 1], matrix[y + 2][x]])
        if (diag1 in matches) and (diag2 in matches):
            total += 1

print(total)
