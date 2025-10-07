from sys import argv
from collections import deque, defaultdict
from math import log2
from itertools import combinations


def read(path):
    wires = {}
    gates = {}

    with open(path) as file:
        part1, part2 = file.read().strip().split("\n\n")

    for line in part1.split("\n"):
        id, val = line.strip().split(":")
        wires[id.strip()] = int(val.strip())

    for line in part2.split("\n"):
        in1, op, in2, _, out = line.strip().split()
        gates[out] = (op, in1, in2, out)

    return wires, gates


def wire_key(prefix, num):
    return f"{prefix}{num:02}"


def get_wires_for(num, prefix, bitlen):
    res = {}
    for i, b in enumerate(reversed(f"{num:0{bitlen}b}")):
        res[wire_key(prefix, i)] = int(b)
    return res


def compute(wires, gates):
    res = 0
    outputs = [k for k in gates.keys() if k[0] == "z" and int(k[1:]) >= 0]
    for out in sorted(outputs, reverse=True):
        res = (res << 1) + compute_output(out, wires, gates, set())
    return res


def compute_output(out, wires, gates, seen):
    if out in seen:
        raise RuntimeError("Cycle detected")

    seen.add(out)

    if out in wires:
        return wires[out]

    op, in1, in2, out = gates[out]

    if in1 not in wires:
        wires[in1] = compute_output(in1, wires, gates, seen)
    if in2 not in wires:
        wires[in2] = compute_output(in2, wires, gates, seen)

    return run_operation(op, wires[in1], wires[in2])


def run_operation(op_code, in1, in2):
    if op_code == "AND":
        return in1 & in2
    elif op_code == "OR":
        return in1 | in2
    elif op_code == "XOR":
        return in1 ^ in2
    assert False, f"{op_code} not a valid operation, must be on of AND, OR, XOR"


def validate_initial_xor(out, pos, gates):
    if out not in gates:
        return False

    op, in1, in2, _ = gates[out]
    if op != "XOR":
        return False

    return sorted([in1, in2]) != [wire_key("x", pos), wire_key("y", pos)]


def validate_initial_and(out, pos, gates):
    if out not in gates:
        return False

    op, in1, in2, _ = gates[out]
    if op != "AND":
        return False

    return sorted([in1, in2]) != [wire_key("x", pos), wire_key("y", pos)]


def validate_intermediate_and(out, pos, gates):
    if out not in gates:
        return False

    op, in1, in2, _ = gates[out]
    if op != "AND":
         return False

    return

def validate_carry_over(out, pos, gates):
    if out not in gates:
        return False

     op, in1, in2, _ = gates[out]
     if op != "OR":
         return False


def validate_circuit(pos, gates):
    out = wire_key(pos, "z")

    if out not in gates:
        return False

    op, in1, in2, _ = gates[out]
    if op != "XOR":
        return False

    return (
        validate_initial_xor(in1, pos, gates)
        and validate_intermediate_and(in2, pos, gates)
        or validate_initial_xor(in2, pos, gates)
        and validate_intermediate_and(in1, pos, gates)
    )


def find_first_problem(gates, debug=True):
    bitlen = 45
    for i in range(bitlen):
        num = (1 << i + 1) + 1
        wires = get_wires_for(num, "x", bitlen)
        wires |= get_wires_for(num, "y", bitlen)
        have = compute(wires, gates)
        want = 2 * num
        if have != want:
            err_pos = least_significant_set_bit(have ^ want)
            if debug:
                print(f"Problem with z{err_pos:02}")
            return err_pos

    if debug:
        print("No problems found")

    return None


def least_significant_set_bit(num):
    return int(log2(num & -num))


def gates_by_input(gates):
    res = defaultdict(list)
    for _, in1, in2, out in gates.values():
        res[in1].append(out)
        res[in2].append(out)
    return res


def get_all_gates(pos, lookup):
    res = []
    q = deque([(wire_key("x", pos), 0)])
    while q:
        curr, d = q.pop()
        if d > 1:
            continue
        for nxt in lookup[curr]:
            res.append(nxt)
            q.append((nxt, d + 1))

    return sorted(res)


orig_wires, gates = read(argv[1])

lookup = gates_by_input(gates)
swaps = []
while prev := find_first_problem(gates):
    gate_pairs = combinations(get_all_gates(prev, lookup), 2)
    after = prev
    for a, b in gate_pairs:
        gates[a], gates[b] = gates[b], gates[a]

        try:
            after = find_first_problem(gates)
            if after == None or after > prev:
                # Successful swap
                print(prev, "Successful Swap:", (a, b))
                swaps.extend([a, b])
                break
            else:
                print(prev, "Unsuccessful Swap:", (a, b))
        except:
            print(prev, "Invalid Swap:", (a, b))
            # Invalid swap
            pass

        # Invalid or unsuccessful, swap back
        gates[a], gates[b] = gates[b], gates[a]

    if after is not None and after <= prev:
        print("Giving up")
        # not able to fix this problem
        break

print(find_first_problem(gates))
print(",".join(sorted(swaps)))


def get_number(prefix, wires):
    res = []
    for out in sorted(filter(lambda k: k[0] == prefix, wires.keys()), reverse=True):
        res.append(str(wires[out]))
    res = "".join(res)
    return int(res, 2)


x = get_number("x", orig_wires)
y = get_number("y", orig_wires)
want = x + y
have = compute(orig_wires, gates)
diff = want ^ have
print(f"WANT: {want:046b}")
print(f"HAVE: {have:046b}")
print(f"DIFF: {diff:046b}")
print(least_significant_set_bit(diff))

# gqp,hsw,jmh,kqf,mwk,qgd,z18,z33
# gqp,hsw,jmh,mwk,qgd,z10,z18,z33

# kqf,mwk
