from sys import argv


def find_space(size: int, free: list[tuple[int, int]]) -> int:
    for i, (_, sz) in enumerate(free):
        if sz >= size:
            return i
    return -1


files: list[tuple[int, int, int]] = []
free: list[tuple[int, int]] = []
pos = 0
with open(argv[1], "r") as file:
    for i, c in enumerate(map(int, file.read().strip())):
        if c == 0:
            continue

        if i % 2 == 0:
            id = i // 2
            files.append((id, pos, c))
        else:
            id = -1
            free.append((pos, c))

        pos += c

files.reverse()
for i, (id, file_pos, file_size) in enumerate(files):
    free_index = find_space(file_size, free)
    if free_index >= 0:
        free_pos, free_size = free[free_index]
        if free_pos < file_pos:
            if free_size - file_size == 0:
                del free[free_index]
            else:
                free[free_index] = (free_pos + file_size, free_size - file_size)
            files[i] = (id, free_pos, file_size)

total = 0
for id, pos, filesize in files:
    for i in range(filesize):
        total += (pos + i) * id
print(total)
