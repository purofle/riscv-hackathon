from machine import get_reg, set_reg
from utils import bytes_to_int


class RType:
    def __init__(self, inst: int):
        self.rd     = (inst >> 7) & 0x1F
        self.funct3 = (inst >> 12) & 0x7
        self.rs1    = (inst >> 15) & 0x1F
        self.rs2    = (inst >> 20) & 0x1F
        self.funct7 = (inst >> 25) & 0x7F

        self.rs1_value = bytes_to_int(get_reg(self.rs1))
        self.rs2_value = bytes_to_int(get_reg(self.rs2))
        
        self.funct3_map = {
            0b000: self.add,
            0b100: self.xor,
        }

    def __str__(self):
        return f"RType(funct3={self.funct3}, funct7={self.funct7}, rs1={self.rs1}, rs2={self.rs2}, rd={self.rd})"
    
    def execute(self):
        # Execute the instruction based on funct3
        if self.funct3 in self.funct3_map:
            self.funct3_map[self.funct3]()
        else:
            print(f"Unknown R-Type instruction with funct3: {self.funct3}")
    
    def add(self):
        result = (self.rs1_value + self.rs2_value) & 0xF # 忽略算数溢出
        set_reg(self.rd, result.to_bytes(4, byteorder='little'))
        print(f"ADD: x{self.rs1} + x{self.rs2} = {result} -> x{self.rd}")

    def xor(self):
        result = self.rs1_value ^ self.rs2_value
        set_reg(self.rd, result.to_bytes(4, byteorder='little'))
        print(f"XOR: x{self.rs1} ^ x{self.rs2} = {result} -> x{self.rd}")