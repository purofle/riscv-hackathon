from machine import get_pc, set_reg, set_pc
from utils import sign_extend


class JType:
    def __init__(self, inst: int):
        self.opcode = inst & 0x7F
        self.rd = (inst >> 7) & 0x1F
        imm_19_12 = (inst >> 12) & 0xFF
        imm_11 = (inst >> 20) & 0x1
        imm_10_1 = (inst >> 21) & 0x3FF
        imm_20 = (inst >> 31) & 0x1

        # 拼接立即数
        self.imm = (imm_20 << 20) | (imm_19_12 << 12) | (imm_11 << 11) | (imm_10_1 << 1)
        self.offset = sign_extend(self.imm & 0xFFF, 12)

    def __str__(self):
        return f"JType: imm={self.imm}, offset={self.offset}"

    def execute(self):
        match self.opcode:
            case 0b1101111:
                set_reg(self.rd, get_pc() + 4)
                set_pc(get_pc() + self.offset)