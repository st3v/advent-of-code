from sys import argv
from collections import defaultdict


def in_key(in1, in2):
    return ":".join(sorted([in1, in2]))


def read(path):
    wires = {}
    gates = defaultdict()

    with open(path) as file:
        part1, part2 = file.read().strip().split("\n\n")

    for line in part1.split("\n"):
        id, val = line.strip().split(":")
        wires[id.strip()] = int(val.strip())

    for line in part2.split("\n"):
        # ntg XOR fgs -> mjb
        in1, op, in2, _, out = line.strip().split()
        # in1, in2 = sorted([in1, in2])
        gates[out] = (op, in1, in2, out)
        # gates[in2].append((op, in1, in2, out))

    return wires, gates


def render(out, gates, d=0):
    if out not in gates or d > 2:
        return out

    op, in1, in2, out = gates[out]
    left = render(in1, gates, d + 1)
    right = render(in2, gates, d + 1)
    if len(left) > len(right):
        left, right = right, left
    return f"[ {left} ] {op} [ {right} ]"


wires, gates = read(argv[1])

seen = set()
for out in sorted(gates.keys()):
    if out[0] != "z" or out in seen:
        continue
    seen.add(out)
    print(f"{out} = [ {render(out, gates)} ]")
    # print()

# x = [k for k in wires.keys() if k[0] == "x"]
# y = [k for k in wires.keys() if k[0] == "y"]

# unexpected_gates = {}
# for a, b in zip(x, y):
#     a, b = sorted([a, b])
#     print(a, b)
#     outs = []
#     for op, in1, in2, out in sorted(gates[a], key=lambda g: g[0], reverse=True):
#         if in1 == a and in2 == b:
#             branch = [op + " ["]
#             # print(f"  {in2} {op} {in2} = {out}")
#             if out not in gates:
#                 branch.append(f"{out}")
#             prev = out
#             for op, in1, in2, out in sorted(gates[out], key=lambda g: g[0]):
#                 branch.append(f"{prev}: {op} [")
#                 # print(f"    {in1} {op} {in2} = {out}")
#                 if out not in gates:
#                     branch.append(f"{out}")
#                 prev2 = out
#                 for op, in1, in2, out in sorted(gates[out], key=lambda g: g[0]):
#                     branch.append(f"{prev2}: {op} [ {out} ]")
#                     # print(f"      {in1} {op} {in2} = {out}")
#                 branch.append("]")
#             branch.append("]")
#             print(" ".join(branch))
#         else:
#             unexpected_gates.append((op, in1, in2, out))


print(",".join(sorted(["hsw", "jmh", "z18", "qgd", "mwk", "z10", "gqp", "z33"])))
