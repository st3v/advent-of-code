from sys import argv

wires = {}
gates = set()

with open(argv[1]) as file:
    part1, part2 = file.read().strip().split("\n\n")

for line in part1.split("\n"):
    id, val = line.strip().split(":")
    wires[id.strip()] = int(val.strip())

for line in part2.split("\n"):
    # ntg XOR fgs -> mjb
    in1, op, in2, _, out = line.strip().split()
    gates.add((op, in1, in2, out))

computed = set()
while len(computed) != len(gates):
    for op, in1, in2, out in gates:
        if in1 in wires and in2 in wires:
            computed.add((op, in1, in2, out))
            if op == "AND":
                wires[out] = (wires[in1] + wires[in2]) // 2
            elif op == "OR":
                wires[out] = (wires[in1] + wires[in2] + 1) // 2
            else:
                wires[out] = abs(wires[in1] - wires[in2])

res = 0
for out in sorted(filter(lambda k: k[0] == "z", wires.keys()), reverse=True):
    res = (res << 1) + wires[out]

print(res)
