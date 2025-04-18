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
            0x0: self.add if self.funct7 == 0 else self.sub,
            0x4: self.xor,
            0x6: self._or,
            0x7: self._and,
            0x1: self.sll,
            0x5: self.srl,
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
        result = (self.rs1_value + self.rs2_value)
        set_reg(self.rd, result)

    def sub(self):
        result = (self.rs1_value - self.rs2_value)
        set_reg(self.rd, result)

    def xor(self):
        result = self.rs1_value ^ self.rs2_value
        set_reg(self.rd, result)

    # shit Python
    def _or(self):
        result = self.rs1_value | self.rs2_value
        set_reg(self.rd, result)

    def _and(self):
        result = self.rs1_value & self.rs2_value
        set_reg(self.rd, result)

    def sll(self):
        result = self.rs1_value << self.rs2_value
        set_reg(self.rd, result)

    def srl(self):
        result = self.rs1_value >> self.rs2_value
        set_reg(self.rd, result)