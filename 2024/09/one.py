from sys import argv

blocks: list[int] = []
with open(argv[1], "r") as file:
    for i, c in enumerate(map(int, file.read().strip())):
        id = i // 2 if i % 2 == 0 else -1
        blocks.extend([id] * c)

left, right = 0, len(blocks) - 1
while True:
    while left < right and blocks[left] >= 0:
        left += 1

    while right > left and blocks[right] < 0:
        right -= 1

    if left >= right:
        break

    blocks[left], blocks[right] = blocks[right], blocks[left]

total = 0
for i, b in enumerate(blocks):
    if b < 0:
        break
    total += i * b

print(total)
