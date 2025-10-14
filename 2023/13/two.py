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


def find_reflection_line(encodings, expected_smudges):
    line = 0
    while line < len(encodings) - 1:
        line += 1
        left, right = line - 1, line
        smudges = expected_smudges
        while left >= 0 and right < len(encodings):
            diffs = (encodings[left] ^ encodings[right]).bit_count()
            if diffs <= smudges:
                left -= 1
                right += 1
                smudges -= diffs
            else:
                break
        if smudges == 0 and (left < 0 or right == len(encodings)):
            return line
    return 0


total = 0
with open(argv[1]) as file:
    for part in file.read().strip().split("\n\n"):
        pattern = []
        for line in part.strip().split("\n"):
            pattern.append(list(line.strip()))

        rows, cols = encode(pattern)

        if (line := find_reflection_line(rows, 1)) != find_reflection_line(rows, 0):
            total += line * 100

        if (line := find_reflection_line(cols, 1)) != find_reflection_line(cols, 0):
            total += line

print(total)
