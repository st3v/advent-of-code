from sys import argv


def is_digit(s):
    if len(s) != 1:
        return False
    return ord(s) - ord("0") < 10


with open(argv[1]) as file:
    values = map(lambda s: s.strip(), file.readlines())

total = 0
for v in values:
    l, r = 0, len(v) - 1
    while l < r:
        found = True

        if not is_digit(v[l]):
            l += 1
            found = False

        if not is_digit(v[r]):
            r -= 1
            found = False

        if found:
            break

    assert l > r, "No digit found"
    total += int(v[l] + v[r])

print(total)
