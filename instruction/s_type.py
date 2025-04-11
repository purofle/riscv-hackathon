from machine import get_reg, write_memory, print_reg
from utils import bytes_to_int, int_to_bytes, sign_extend


class SType:
    def __init__(self, inst: int):
        self.opcode = inst & 0x7F
        self.funct3 = (inst >> 12) & 0x7
        self.rs1    = (inst >> 15) & 0x1F
        self.rs2    = (inst >> 20) & 0x1F
        self.imm    = ((inst >> 25) & 0x7F) | ((inst >> 7) & 0x1F)

        self.funct3_map = {
            0x0: self.sb,
            0x2: self.sw,
        }

        self.offset = sign_extend(self.imm & 0xFFF, 12)

    def __str__(self):
        return f"SType(funct3={self.funct3}, rs1={self.rs1}, rs2={self.rs2}, imm={self.imm})"

    def sb(self):
        # SB instruction
        rs2_value = get_reg(self.rs2)
        address = bytes_to_int(get_reg(self.rs1)) + self.offset
        print(f"SB: x{self.rs2} -> MEM[{hex(address)}]")
        write_memory(address, rs2_value)

    def sw(self):
        # 取 rs2 低位四个字节
        rs2_value = bytes_to_int(get_reg(self.rs2)) & 0xFFFFFFFF
        rs1 = sign_extend(self.rs1 & 0xFFF, 12)
        address = rs1 + self.offset
        write_memory(address, int_to_bytes(rs2_value))

    def execute(self):
        if self.funct3 in self.funct3_map:
            self.funct3_map[self.funct3]()
        else:
            print(f"Unknown I-Type instruction with funct3: {self.funct3}")