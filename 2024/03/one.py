from sys import argv
import re

with open(argv[1], 'r') as file:
    pairs = re.findall("mul\\(([0-9]{1,3}),([0-9]{1,3})\\)", file.read())

total = sum([int(a) * int(b) for a, b in pairs])

print(total)
