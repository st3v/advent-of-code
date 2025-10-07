from sys import argv
import re

with open(argv[1], 'r') as file:
    parts = file.read().strip().split("don't()")

do = [parts[0]]
for p in parts[1:]:
    do += p.split("do()")[1:]
pairs = re.findall("mul\\(([0-9]{1,3}),([0-9]{1,3})\\)", ''.join(do))

total = sum([int(a) * int(b) for a, b in pairs])

print(total)
