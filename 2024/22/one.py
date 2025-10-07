from sys import argv


def step(num):
    num = (num ^ (num * 64)) % 16777216
    num = (num ^ (num // 32)) % 16777216
    return (num ^ (num * 2048)) % 16777216


def solve(num, steps):
    for _ in range(steps):
        num = step(num)
    return num


total = sum(solve(n, 2000) for n in map(int, open(argv[1]).readlines()))
print(total)
