from machine import get_reg, write_memory
from utils import bytes_to_int


class SType:
    def __init__(self, inst: int):
        self.opcode = inst & 0x7F
        self.funct3 = (inst >> 12) & 0x7
        self.rs1    = (inst >> 15) & 0x1F
        self.rs2    = (inst >> 20) & 0x1F
        self.imm    = ((inst >> 25) & 0x7F) | ((inst >> 7) & 0x1F)

        self.funct3_map = {
            0x0: self.sb,
        }

        if self.imm & (1 << 12):
            self.offset = self.imm - (1 << 13)
        else:
            self.offset = self.imm

    def sb(self):
        # SB instruction
        rs2_value = get_reg(self.rs2)
        address = bytes_to_int(get_reg(self.rs1)) + self.offset
        print(f"SB: x{self.rs2} -> MEM[{hex(address)}]")
        write_memory(address, rs2_value)

    def execute(self):
        if self.funct3 in self.funct3_map:
            self.funct3_map[self.funct3]()
        else:
            print(f"Unknown I-Type instruction with funct3: {self.funct3}")