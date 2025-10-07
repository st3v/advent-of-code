from collections import Counter

with open('input.txt', 'r') as file:
    pairs = (map(int, line.strip().split('   ')) for line in file)
    left, right = map(list, zip(*pairs))

counts = Counter(right)
total = sum(l * counts[l] for l in left)

print(total)
