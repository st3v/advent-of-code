from sys import argv
import timeit
import math

with open(argv[1]) as file:
    time = 0
    record = 0
    for line in file:
        key, data = line.strip().split(":")
        key = key.strip()
        data = [d.strip() for d in data.strip().split()]
        data = int("".join(data))
        if key == "Time":
            time = data
        elif key == "Distance":
            record = data


def solve_a(time, record):
    total = 0
    for seconds in range(record // time, time - 1):
        distance = (time - seconds) * seconds
        if distance > record:
            total += 1
    print(total)


def solve_b(time, record):
    left, right = record // time, time - 1
    while left < right:
        changed = False

        if (time - left) * left <= record:
            left += 1
            changed = True

        if (time - right) * right <= record:
            right -= 1
            changed = True

        if not changed:
            break
    print(left, right)
    print(right - left + 1)


def solve_c(time, record):
    for seconds in range(record // time, time - 1):
        distance = (time - seconds) * seconds
        if distance > record:
            print(1 + time - 2 * seconds)
            return


t1 = timeit.timeit(lambda: solve_a(time, record), number=1)
print(f"Solution A: {t1:.2f} seconds")
t2 = timeit.timeit(lambda: solve_b(time, record), number=1)
print(f"Solution B: {t2:.2f} seconds")
t3 = timeit.timeit(lambda: solve_c(time, record), number=1)
print(f"Solution C: {t3:.2f} seconds")
