from machine import get_reg, set_reg, print_reg
from utils import bytes_to_int, int_to_bytes


class IType:
    def __init__(self, inst: int):
        self.opcode = inst & 0x7F
        self.rd     = (inst >> 7) & 0x1F
        self.funct3 = (inst >> 12) & 0x7
        self.rs1    = (inst >> 15) & 0x1F
        self.imm    = (inst >> 20) & 0xFFF
        
        self.funct3_map = {
            0x0: self.addi,
            0x4: self.xori,
            0x6: self.ori,
            0x7: self.andi,
            0x1: self.slli,
            # srli: imm[5:11]=0x00
            0x5: self.srli if (self.imm >> 5) & 0x3F == 0 else self.srai,
        }
        
    def __str__(self):
        return f"IType: funct3={self.funct3}, rs1={self.rs1}, rd={self.rd}, imm={self.imm}"

    def addi(self):
        # ADDI instruction
        rs1_value = bytes_to_int(get_reg(self.rs1))
        rd_value = rs1_value + self.imm
        set_reg(self.rd, rd_value)

    def xori(self):
        # XORI instruction
        rs1_value = bytes_to_int(get_reg(self.rs1))
        rd_value = rs1_value ^ self.imm
        set_reg(self.rd, rd_value)

    def ori(self):
        # ORI instruction
        rs1_value = bytes_to_int(get_reg(self.rs1))
        rd_value = rs1_value | self.imm
        set_reg(self.rd, rd_value)

    def andi(self):
        # ANDI instruction
        rs1_value = bytes_to_int(get_reg(self.rs1))
        rd_value = rs1_value & self.imm
        set_reg(self.rd, rd_value)

    def slli(self):
        # SLLI instruction
        rs1_value = bytes_to_int(get_reg(self.rs1))
        rd_value = rs1_value << (self.imm & 0xF)
        set_reg(self.rd, rd_value)

    def srli(self):
        # SRLI instruction
        rs1_value = bytes_to_int(get_reg(self.rs1))
        rd_value = rs1_value >> (self.imm & 0xF)
        set_reg(self.rd, rd_value)

    def srai(self):
        # SRAI instruction
        rs1_value = bytes_to_int(get_reg(self.rs1))
        rd_value = (rs1_value >> self.imm) | ((rs1_value & (1 << 31)) * ((1 << 32) - 1))
        set_reg(self.rd, rd_value)

    @staticmethod
    def ecall():
        a0 = bytes_to_int(get_reg(10))
        a1 = bytes_to_int(get_reg(11))
        if a0 == 1:
            print(a1)
        elif a0 == 0:
            for i in range(32):
                print(f"x{i}: {hex(bytes_to_int(get_reg(i)))}", end=' ')
        else:
            print(f"Unknown ecall: {a0}, {a1}")

    def load(self):
        match self.funct3:
            case 0x0:
                offset = self.imm
                addr = bytes_to_int(get_reg(self.rs1)) + (offset | 0xffffff00)
                data = bytes_to_int(get_reg(addr))
                set_reg(self.rd, data)

    def execute(self):
        if self.opcode == 0b1110011:
            if self.imm == 0x0:
                self.ecall()
            elif self.imm == 0x1:
                print("EBREAK")
            else:
                print("Unknown system call")
            return
        if self.opcode == 0b0000011:
            self.load()
        # Execute the instruction based on funct3
        elif self.funct3 in self.funct3_map:
            self.funct3_map[self.funct3]()
        else:
            print(f"Unknown I-Type instruction with funct3: {self.funct3}")