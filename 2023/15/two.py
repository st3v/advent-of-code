from sys import argv
import re


def hash(str):
    res = 0
    for s in str:
        res = ((res + ord(s)) * 17) % 256
    return res


total = 0
boxes = [{} for _ in range(256)]
with open(argv[1]) as file:
    for line in file:
        for s in line.strip().split(","):
            id, op, focal_len = re.findall(r"([a-zA-Z]*)([\-\=])([0-9]*)", s.strip())[0]
            key = hash(id)
            if op == "=":
                pos = boxes[key][id][1] if id in boxes[key] else len(boxes[key]) + 1
                boxes[key][id] = (int(focal_len), pos)
            elif op == "-" and id in boxes[key]:
                _, pos = boxes[key][id]
                del boxes[key][id]
                for i, (l, p) in boxes[key].items():
                    if p > pos:
                        boxes[key][i] = (l, p - 1)

total = 0
for i, box in enumerate(boxes):
    for lense, (focal_len, slot) in box.items():
        total += (i + 1) * focal_len * slot
print(total)
