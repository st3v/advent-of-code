a, b = [], []

with open('input.txt', 'r') as file:
    for line in file:
        parts = line.strip().split('   ')
        a.append(parts[0])
        b.append(parts[1])

a.sort()
b.sort()

diff = 0
for a, b in zip(a, b):
    diff += abs(int(a) - int(b))

print(diff)
