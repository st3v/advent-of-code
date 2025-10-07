from sys import argv


class Node:
    def __init__(self, data: int):
        self.data: int = data
        self.prev: Node | None = None
        self.next: Node | None = None

    def transition(self) -> int:
        if self.data == 0:
            self.data = 1
            return 1

        if self.data_len() % 2 == 0:
            self.split()
            return 2

        self.data *= 2024
        return 1

    def split(self):
        c = list(str(self.data))
        self.data = int("".join(c[0 : len(c) // 2]))

        right = Node(int("".join(c[len(c) // 2 :])))
        right.prev = self
        if self.next:
            right.next = self.next
            self.next.prev = right

        self.next = right

    def data_len(self):
        return len(str(self.data))


prev: Node | None = None
head: Node | None = None
with open(argv[1], "r") as file:
    for stone in list(map(int, file.read().strip().split(" "))):
        node = Node(stone)
        if prev:
            prev.next = node
            node.prev = prev
        else:
            head = node
        prev = node

total = 0
for _ in range(25):
    node = head
    total = 0
    while node:
        next = node.next
        total += node.transition()
        node = next

print(total)
