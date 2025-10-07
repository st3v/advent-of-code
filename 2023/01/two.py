from sys import argv


def digit(s):
    if not s:
        return None

    if (d := ord(s[0]) - ord("0")) < 10:
        return d

    return prefix_to_digit(s)


def prefix_to_digit(s):
    digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for d, w in enumerate(digits):
        if s.startswith(w):
            return d + 1
    return None


with open(argv[1]) as file:
    values = map(lambda s: s.strip(), file.readlines())

total = 0
for v in values:
    left, right = None, None
    l, r = 0, len(v) - 1
    while l <= r + 1:
        if left is None:
            left = digit(v[l:])
            l += 1

        if right is None:
            right = digit(v[r:])
            r -= 1

        if left is not None and right is not None:
            break

    assert left is not None and right is not None, f"No two digits found for {v}"

    total += left * 10 + right

print(total)
