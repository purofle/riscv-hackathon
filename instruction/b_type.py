from machine import get_reg, set_pc, get_pc
from utils import bytes_to_int


class BType:
    def __init__(self, inst: int):
        self.imm11   = (inst >> 7) & 0x1
        self.imm4_1  = (inst >> 8) & 0xF
        self.funct3  = (inst >> 12) & 0x7
        self.rs1     = (inst >> 15) & 0x1F
        self.rs2     = (inst >> 20) & 0x1F
        self.imm10_5 = (inst >> 25) & 0x3F
        self.imm12   = (inst >> 31) & 0x1

        self.rs1_value = bytes_to_int(get_reg(self.rs1))
        self.rs2_value = bytes_to_int(get_reg(self.rs2))

        self.offset = (self.imm12 << 12) | (self.imm11 << 11) | (self.imm10_5 << 5) | (self.imm4_1 << 1)

        if self.offset & (1 << 12):
            self.offset = self.offset - (1 << 13)

        self.funct3_map = {
            0x1: self.bne,
            0x4: self.blt,
            0x0: self.beq,
        }

    def __str__(self):
        return f"BType(funct3={self.funct3}, rs1={self.rs1}, rs2={self.rs2}, imm11={self.imm11}, imm4_1={self.imm4_1}, imm10_5={self.imm10_5}, imm12={self.imm12})"

    def execute(self):
        # Execute the instruction based on funct3
        if self.funct3 in self.funct3_map:
            self.funct3_map[self.funct3]()
        else:
            print(f"Unknown B-Type instruction with funct3: {self.funct3}")

    def blt(self):
        if self.rs1_value < self.rs2_value:
            new_pc = get_pc() + self.offset
            print(f"BLT: x{self.rs1} < x{self.rs2} -> PC: {hex(get_pc())} + {self.offset} = {hex(new_pc)}")
            set_pc(new_pc)
        else:
            print("BLT: No branch taken")

    def bne(self):
        if self.rs1_value != self.rs2_value:
            new_pc = get_pc() + self.offset
            print(f"BNE: x{self.rs1} != x{self.rs2} -> PC: {hex(get_pc())} + {self.offset} = {hex(new_pc)}")
            set_pc(new_pc)
        else:
            print("BNE: No branch taken")

    def beq(self):
        if self.rs1_value == self.rs2_value:
            new_pc = get_pc() + self.offset
            print(f"BEQ: x{self.rs1} == x{self.rs2} -> PC: {hex(get_pc())} + {self.offset} = {hex(new_pc)}")
            set_pc(new_pc)
        else:
            print("BEQ: No branch taken")