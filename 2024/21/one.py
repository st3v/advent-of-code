from sys import argv
from collections import deque
from itertools import permutations


def read(path):
    with open(path, "r") as file:
        return [l.strip() for l in file.readlines()]


def find_key(key, keypad):
    for x in range(len(keypad)):
        for y in range(len(keypad[0])):
            if keypad[x][y] == key:
                return x, y
    assert False, f"Key {key} not found in keypad {keypad}"


def sequence_valid(sequence, start, keypad):
    """
    A sequence of directions is valid if it does not go over the
    None key on the keypad we are navigating.
    """
    dirs = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0), "A": (0, 0)}
    x, y = find_key(start, keypad)
    for k in sequence:
        dx, dy = dirs[k]
        x, y = x + dx, y + dy
        if not (0 <= x < len(keypad) and 0 <= y < len(keypad[0])):
            # print(f"Left keypad: {sequence}")
            return False

        if not keypad[x][y]:  # None key
            # print(f"Hit None: {sequence}")
            return False
    return True


def find_sequence(start, end, keypad):
    sequence = []
    visited = set()
    q = deque([(*find_key(start, keypad), "")])
    while q:
        x, y, sequence = q.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if keypad[x][y] == end:
            return sequence

        for dx, dy, dir in [(0, 1, ">"), (1, 0, "v"), (0, -1, "<"), (-1, 0, "^")]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < len(keypad) and 0 <= ny < len(keypad[0])):
                continue

            if not keypad[nx][ny] or (nx, ny) in visited:
                continue

            q.append((nx, ny, sequence + dir))

    return None


def key_presses(sequence, keypad):
    current = find_key("A", keypad)
    assert current is not None

    res = []
    prev = "A"
    for curr in sequence:
        seq = find_sequence(prev, curr, keypad)
        opts = valid_orderings(seq, prev, keypad)
        assert seq is not None, f"{prev}, {curr}, {sequence}"
        res.append(opts)
        prev = curr

    return res


def valid_orderings(sequence, start, keypad):
    if len(set(sequence)) < 2:
        return [sequence + "A"]

    res = set()
    orderings = permutations(list(">^v<"))
    for o in orderings:
        index = {d: i for i, d in enumerate(o)}
        s = "".join(sorted(sequence, key=lambda k: index[k])) + "A"
        if sequence_valid(s, start, keypad):
            res.add(s)

    return list(res)


def decode(sequence, keypads):
    for keypad in reversed(keypads + [directional]):
        sequence = press_keys(sequence, keypad)
    return sequence


def encode(sequence, keypads):
    for i, keypad in enumerate(keypads):
        candidates = key_presses(sequence, keypad)
        chosen = []
        for sequences in candidates:
            optimal = encode(sequences[0], keypads[i + 1 :])
            for s in sequences[1:]:
                final = encode(s, keypads[i + 1 :])
                if len(final) < len(optimal):
                    optimal = final
            chosen.append(optimal)
        old, new = sequence, "".join(chosen)
        sequence = new
    return sequence


def press_keys(sequence, keypad):
    current = find_key("A", keypad)
    assert current is not None

    res = []
    dirs = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
    x, y = current
    for k in sequence:
        if k == "A":
            res.append(keypad[x][y])
            continue

        dx, dy = dirs[k]
        x, y = x + dx, y + dy
        assert 0 <= x < len(keypad) and 0 <= y < len(
            keypad[0]
        ), f"Invalid sequence: {sequence}, left keypad {(x, y)}"

        assert keypad[x][y] is not None, f"Invalid sequence: {sequence}, hit None"

    return "".join(res)


codes = read(argv[1])
numeric = [("7", "8", "9"), ("4", "5", "6"), ("1", "2", "3"), (None, "0", "A")]
directional = [(None, "^", "A"), ("<", "v", ">")]
keypads = [numeric, directional]

total = 0
for code in codes:
    sequence = encode(code, keypads)
    assert (
        decode(sequence, keypads) == code
    ), f"Invalid sequence {sequence} generated for {code}"
    total += int(code[:-1]) * len(sequence)

print(total)

from itertools import permutations

transitions = {}
for start, end in permutations(list("A>^v<A>^v<"), 2):
    if start == end:
        transitions[(start, end)] = ""
    else:
        transitions[(start, end)] = find_sequence(start, end, directional)


chains = [transitions]

for i in range(1, 3):
    next = {}
    for start, end in permutations(list("A>^v<A>^v<"), 2):
        if start == end:
            next[(start, end)] = ""
            continue

        curr = []
        prev = chains[i - 1][(start, end)]
        for s, e in zip("A" + prev, prev):
            curr.append(chains[0][(s, e)])
        next[start, end] = "A".join(curr) + "A"
    chains.append(next)


def encode_new(directional_sequence, chain_len=2):
    res = []
    start = "A"
    for end in directional_sequence:
        res.append(chains[chain_len - 1][(start, end)])
        start = end
    return "".join(res)


from itertools import product


def optimize_list(sequences):
    res = []
    for s in sequences:
        res.append(optimize_sequence(s))

    return res


def optimize_sequence(sequence):
    if len(set(sequence)) < 2:
        return sequence

    optimal = sequence
    min = len(encode_new(sequence))

    orderings = permutations(list(">^v<"))
    for o in orderings:
        index = {d: i for i, d in enumerate(o)}
        candidate = "".join(sorted(sequence, key=lambda k: index[k]))
        if (l := len(encode_new(candidate))) < min:
            l = min
            optimal = candidate

    return optimal


res = []
code = "379A"
start = "A"
for end in code:
    res.append(find_sequence(start, end, numeric))
    start = end
first = "A".join(optimize_list(res)) + "A"


# total = 0
# for code in codes:
#     orig = code

#     num = int(code[:-1])
#     # print(code)
#     # depth = 2
#     for keypad in keypads:
#         code = key_presses(code, keypad)
#         assert code is not None, "code is None"
#         # print(f"{' '*depth}{code}")
#         # depth += 2

#     total += num * len(code)
#     print(num, len(code), code)
#     # depth -= 4
#     for keypad in reversed(keypads):
#         code = press_keys(code, keypad)
#         # print(f"{' '*depth}{code}")
#         # depth -= 2

#     assert orig == code, "Invalid"

# print(total)


# mine = "v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A>^AA<A>Av<A<A>>^AAAvA^<A>A"
# theirs = "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"

# for keypad in reversed(keypads):
#     print(f"mine:   {mine}\ntheirs: {theirs}")
#     mine = press_keys(mine, keypad)
#     theirs = press_keys(theirs, keypad)
# print(f"mine:   {mine}\ntheirs: {theirs}")

"""

7 8 9
4 5 6
1 2 3
_ 0 A

_ ^ A
< v >

mine:   v<<A>>^AvA^A v<<A>>^AAv<A<A>>^AAvAA^<A>A v<A>^AA<A>A v<A<A>>^AAAvA^<A>A
mine:   <A>A         <AAv<AA>>^A                 vAA^A       v<AAA>^A
mine:   ^A           ^^<<A                       >>A         vvvA
mine:   3            7                           9           A

v<<AA>>^AAAv<AA<AA>>^AAAAvA<^AA>AAAvA^AAv<AA^>AAAAv<AA<A>>^AAAAAA

theirs: <v<A>>^AvA^A <vA<AA>>^AAvA<^A>AAvA^A     <vA>^AA<A>A <v<A>A>^AAAvA<^A>A
theirs: <A>A         v<<AA>^AA>A                 vAA^A       <vAAA>^A
theirs: ^A           <<^^A                       >>A         vvvA
theirs: 3            7                           9           A



mine:   <A>A <AAv<AA>>^A vAA^A v<AAA>^A
theirs: <A>A v<<AA>^AA>A vAA^A <vAAA>^A
mine:   ^A   ^^<<A       >>A   vvvA
theirs: ^A   <<^^A       >>A   vvvA
mine:   3    7           9     A
theirs: 3    7           9     A

"""
