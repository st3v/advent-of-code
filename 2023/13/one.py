from sys import argv


def encode(pattern):
    if not pattern:
        return [], []

    rows = [0 for _ in range(len(pattern))]
    cols = [0 for _ in range(len(pattern[0]))]

    for r in range(len(pattern)):
        for c in range(len(pattern[r])):
            rows[r] <<= 1
            rows[r] += 1 if pattern[r][c] == "#" else 0
            cols[c] <<= 1
            cols[c] += 1 if pattern[r][c] == "#" else 0

    return rows, cols


def find_reflection_line(encodings):
    line = 0
    while line < len(encodings) - 1:
        line += 1
        left, right = line - 1, line
        while left >= 0 and right < len(encodings):
            if encodings[left] == encodings[right]:
                left -= 1
                right += 1
            else:
                break
        if left < 0 or right == len(encodings):
            return line
    return 0


total = 0
with open(argv[1]) as file:
    for part in file.read().strip().split("\n\n"):
        pattern = []
        for line in part.strip().split("\n"):
            pattern.append(list(line.strip()))
        rows, cols = encode(pattern)
        total += find_reflection_line(rows) * 100
        total += find_reflection_line(cols)
print(total)
