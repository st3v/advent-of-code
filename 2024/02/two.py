from sys import argv


def isSafe(report: list[int], skip=True) -> bool:
    if len(report) < 2:
        return True

    if report[0] < report[1]:
        dir = 1
    elif report[0] > report[1]:
        dir = -1
    else:
        if not skip:
            return False
        else:
            return \
                isSafe(report[1:], False) or \
                isSafe(report[:1]+report[2:], False)

    for i, (prev, curr) in enumerate(zip(report, report[1:])):
        diff = (curr - prev) * dir
        if not (0 < diff < 4):
            if skip:
                return \
                    isSafe(report[:i+1]+report[i+2:], False) or \
                    isSafe(report[:i]+report[i+1:], False) or \
                    isSafe(report[:max(0,i-1)]+report[i:], False)
            else:
                return False

    return True

with open(argv[1], 'r') as file:
    reports = [list(map(int, line.strip().split(' '))) for line in file]

safe = sum(1 for r in reports if isSafe(r))
print(safe)

# [a, b, c, d, e]
#        ^
#
# [a, b, x, d, e]
#     `-----'
#
# [a, x, c, d, e]
#  `-----'
#
# [x, b, c, d, e]
#     `--'
