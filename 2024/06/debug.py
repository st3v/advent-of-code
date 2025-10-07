go: set[str] = set()
with open("go.output.txt", "r") as file:
    for line in file:
        go.add(line.strip())

py: set[str] = set()
with open("py.output.txt", "r") as file:
    for line in file:
        py.add(line.strip())

missing = 0
for e in go:
    if e not in py:
        missing += 1
        # print(">", e)

unexpected = 0
matching = 0
for e in py:
    if e not in go:
        unexpected += 1
        # print("<", e)
    else:
        matching += 1

print(f"matches: {matching}\nmissing: {missing}\nunexpected: {unexpected}")
