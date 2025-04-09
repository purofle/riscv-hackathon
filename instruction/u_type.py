from machine import set_reg


class UType:
    def __init__(self, inst: int):
        self.rd = (inst >> 7) & 0x1F
        self.imm = (inst >> 12) & 0xFFFFF

    def lui(self):
        # LUI instruction
        imm_value = self.imm << 12
        set_reg(self.rd, imm_value.to_bytes(4, byteorder='little'))
        print(f"LUI: {self.imm} = {imm_value} -> x{self.rd}")
