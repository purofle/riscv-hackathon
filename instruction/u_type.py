from machine import set_reg


class UType:
    def __init__(self, inst: int):
        self.rd = (inst >> 7) & 0x1F
        self.imm = (inst >> 12) & 0xFFFFF

    def __str__(self):
        return f"LUI: {self.imm} = {self.imm << 12} -> x{self.rd}"


    def lui(self):
        # LUI instruction
        imm_value = self.imm << 12
        set_reg(self.rd, imm_value)
