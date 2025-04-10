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

        }
        
    def __str__(self):
        return f"IType: funct3={self.funct3}, rs1={self.rs1}, rd={self.rd}, imm={self.imm}"
    
    def addi(self):
        # ADDI instruction
        rs1_value = bytes_to_int(get_reg(self.rs1))
        rd_value = rs1_value + self.imm
        set_reg(self.rd, rd_value)
        print(f"ADDI: x{self.rs1} + {self.imm} = {rd_value} -> x{self.rd}")

    def ecall(self):
        a0 = bytes_to_int(get_reg(10))
        a1 = bytes_to_int(get_reg(11))
        if a0 == 1:
            print(a1)
        elif a0 == 0:
            for i in range(32):
                print(f"x{i}: {hex(bytes_to_int(get_reg(i)))}", end=' ')
        else:
            print(f"Unknown ecall: {a0}, {a1}")

    def execute(self):
        if self.opcode == 0b1110011:
            if self.imm == 0x0:
                self.ecall()
            elif self.imm == 0x1:
                print("EBREAK")
            else:
                print("Unknown system call")
            return
        # Execute the instruction based on funct3
        if self.funct3 in self.funct3_map:
            self.funct3_map[self.funct3]()
        else:
            print(f"Unknown I-Type instruction with funct3: {self.funct3}")