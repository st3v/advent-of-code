from sys import argv


def hash(str):
    res = 0
    for s in str:
        res = ((res + ord(s)) * 17) % 256
    return res


total = 0
with open(argv[1]) as file:
    for line in file:
        for s in line.strip().split(","):
            total += hash(s.strip())
print(total)
