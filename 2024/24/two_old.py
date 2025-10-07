from sys import argv
import copy
from collections import deque


def read(path):
    wires = {}
    gates = {}

    with open(path) as file:
        part1, part2 = file.read().strip().split("\n\n")

    for line in part1.split("\n"):
        id, val = line.strip().split(":")
        wires[id.strip()] = int(val.strip())

    for line in part2.split("\n"):
        # ntg XOR fgs -> mjb
        in1, op, in2, _, out = line.strip().split()
        gates[out] = (op, in1, in2)

    return wires, gates


def get_number(prefix, wires):
    res = []
    for out in sorted(filter(lambda k: k[0] == prefix, wires.keys()), reverse=True):
        res.append(str(wires[out]))
    res = "".join(res)
    return int(res, 2)


def compute(memo, gates):
    wires = copy.copy(memo)
    computed = set()
    while len(computed) != len(gates):
        open = False
        for out, (op, in1, in2) in gates.items():
            if in1 in wires and in2 in wires and (op, in1, in2, out) not in computed:
                open = True
                computed.add((op, in1, in2, out))
                if op == "AND":
                    wires[out] = (wires[in1] + wires[in2]) // 2
                elif op == "OR":
                    wires[out] = (wires[in1] + wires[in2] + 1) // 2
                else:
                    wires[out] = abs(wires[in1] - wires[in2])
        if not open:
            raise RuntimeError("Unexpected: No more open gates")

    x = get_number("x", wires)
    y = get_number("y", wires)
    z = get_number("z", wires)

    return x, y, z


def get_bit(num, bit):
    return (num >> bit) & 1


wires, gates = read(argv[1])

for i in range(45):
    for j in range(45):
        v = 1 if i == j else 0
        wires[f"x{j:02}"] = v
        wires[f"y{j:02}"] = v

    x, y, z = compute(wires, gates)
    want = x + y
    have = z
    if want != have:
        diff = want ^ have
        print(f"Error for {x.bit_length() - 1}:")
        print(f"  want: {want:046b}")
        print(f"  have: {have:046b}")
        print(f"  diff: {diff:046b}")

# want = x + y
# have = z
# diff = want ^ have

# print(f"want: {have:b}")
# print(f"have: {want:b}")
# print(f"diff: {diff:0{(have).bit_length()}b}")

# candidates = set()
# d = diff
# i = 0
# expected = [[], []]
# while d > 0:
#     if d & 1 == 1:
#         out = f"z{i:02}"
#         candidates.add(out)
#         expected[get_bit(have, i)].append(out)
#     d = d >> 1
#     i += 1


# for c in candidates:
#     op, in1, in2 = gates[c]
#     if in1 in gates:
#         op1, in11, in12 = gates[in1]
#         in1 = f"{wires[in11]} {op1} {wires[in12]} = {wires[in1]}"
#     else:
#         in1 = f"{in1} = {wires[in1]}"
#     if in2 in gates:
#         op2, in21, in22 = gates[in2]
#         in2 = f"{wires[in21]} {op2} {wires[in22]} = {wires[in2]}"
#     else:
#         in2 = f"{in2} = {wires[in2]}"
#     b = int(c[1:])
#     print(f"{c}: ({in1}) {op} ({in2}) != {get_bit(want, b)}")

# for a, b in zip(*expected):
#     gates[a], gates[b] = gates[b], gates[a]
#     candidates.remove(a)
#     candidates.remove(b)
