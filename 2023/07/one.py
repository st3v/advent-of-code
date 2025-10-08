from sys import argv
from collections import Counter

hands = []
bids = []
with open(argv[1]) as file:
    for line in file:
        hand, bid = line.strip().split()
        hands.append(hand.strip())
        bids.append(int(bid.strip()))

strength = {s: i for i, s in enumerate(list("23456789TJQKA"))}

rankings = []
for i, h in enumerate(hands):
    counts = Counter()
    points = 0
    for s in h:
        points = points * 13 + strength[s] + 1
        counts[s] += 1

    fingerprint = "".join([str(c) for c in sorted(counts.values())])
    types = {
        f: i + 1 for i, f in enumerate(["11111", "1112", "122", "113", "23", "14", "5"])
    }
    rankings.append((types[fingerprint] * (13**5) + points, i))

rankings = sorted(rankings)

total = 0
for rank, (_, i) in enumerate(rankings):
    total += bids[i] * (rank + 1)
print(total)
