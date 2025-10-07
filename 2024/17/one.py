from sys import argv
from typing import Callable
from dataclasses import dataclass, field


def read(path: str) -> tuple[list[int], list[int]]:
    with open(path, "r") as file:
        regs, prog = file.read().strip().split("\n\n")

    registers: list[int] = []
    for r in regs.split("\n"):
        _, val = r.split(":")
        registers.append(int(val.strip()))

    _, val = prog.split(":")
    return (registers, list(map(int, val.strip().split(","))))


@dataclass
class Computer:
    registers: list[int]
    program: list[int]
    verbose: bool = False
    counter: int = 0
    output: list[str] = field(default_factory=list)

    def info(self, s: str):
        if self.verbose:
            print(s, self.registers, self.counter, ",".join(self.output))

    def op(self) -> Callable[[], None]:
        op_code = self.program[self.counter]
        ops = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]
        return ops[op_code]

    def run(self):
        while self.counter < len(self.program):
            self.op()()
        print(",".join(self.output))

    def literal_operand(self) -> int:
        return self.program[self.counter + 1]

    def combo_operand(self) -> int:
        operand = self.program[self.counter + 1]
        """
        Combo operands 0 through 3 represent literal values 0 through 3.
        Combo operand 4 represents the value of register A.
        Combo operand 5 represents the value of register B.
        Combo operand 6 represents the value of register C.
        Combo operand 7 is reserved and will not appear in valid programs.
        """
        if 0 <= operand < 4:
            return operand
        elif 4 <= operand < 7:
            return self.registers[operand - 4]
        else:
            raise AssertionError(f"invalid combo operand: {operand}")

    def adv(self):
        """
        The adv instruction (opcode 0) performs division. The numerator is the value
        in the A register. The denominator is found by raising 2 to the power of the
        instruction's combo operand. So, an operand of 2 would divide A by 4 (2^2);
        an operand of 5 would divide A by 2^B. The result of the division operation
        is truncated to an integer and then written to the A register.
        """
        self.info("adv")
        self.registers[0] //= pow(2, self.combo_operand())
        self.counter += 2

    def bxl(self):
        """
        The bxl instruction (opcode 1) calculates the bitwise XOR of register B and
        the instruction's literal operand, then stores the result in register B.
        """
        self.info("bxl")
        self.registers[1] ^= self.literal_operand()
        self.counter += 2

    def bst(self):
        """
        The bst instruction (opcode 2) calculates the value of its combo operand
        modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to
        the B register.
        """
        self.info("bst")
        self.registers[1] = self.combo_operand() % 8
        self.counter += 2

    def jnz(self):
        """
        The jnz instruction (opcode 3) does nothing if the A register is 0. However,
        if the A register is not zero, it jumps by setting the instruction pointer to
        the value of its literal operand; if this instruction jumps, the instruction
        pointer is not increased by 2 after this instruction.
        """
        self.info("jnz")
        if self.registers[0] == 0:
            self.counter += 2
        else:
            self.counter = self.literal_operand()

    def bxc(self):
        """
        The bxc instruction (opcode 4) calculates the bitwise XOR of register B and
        register C, then stores the result in register B. For legacy reasons, this
        instruction reads an operand but ignores it.
        """
        self.info("bxc")
        self.registers[1] ^= self.registers[2]
        self.counter += 2

    def out(self):
        """
        The out instruction (opcode 5) calculates the value of its combo operand
        modulo 8, then outputs that value. If a program outputs multiple values,
        they are separated by commas.
        """
        self.info("out")
        self.output.append(str(self.combo_operand() % 8))
        self.counter += 2

    def bdv(self):
        """
        The bdv instruction (opcode 6) works exactly like the adv instruction except
        that the result is stored in the B register. The numerator is still read from
        the A register.
        """
        self.info("bdv")
        self.registers[1] = self.registers[0] // pow(2, self.combo_operand())
        self.counter += 2

    def cdv(self):
        """
        The cdv instruction (opcode 7) works exactly like the adv instruction except
        that the result is stored in the C register. The numerator is still read from
        the A register.
        """
        self.info("cdv")
        self.registers[2] = self.registers[0] // pow(2, self.combo_operand())
        self.counter += 2


comp = Computer(*read(argv[1]))
comp.run()
