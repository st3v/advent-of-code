def isSafe(report: list[int]) -> bool:
    if len(report) < 2:
        return True

    if report[0] < report[1]:
        dir = 1
    elif report[0] > report[1]:
        dir = -1
    else:
        return False

    for prev, curr in zip(report, report[1:]):
        diff = (curr - prev) * dir
        if diff < 1 or diff > 3:
            return False

    return True

with open('input.txt', 'r') as file:
    reports = [list(map(int, line.strip().split(' '))) for line in file]

safe = sum(1 for r in reports if isSafe(r))
print(safe)
