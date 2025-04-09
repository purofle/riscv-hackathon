import sys
from elftools.elf.elffile import ELFFile

from instruction.i_type import IType
from machine import get_memory, get_reg, set_reg, write_memory, pc
from utils import bytes_to_int

def process_file(filename):
    print('Processing file:', filename)
    with open(filename, 'rb') as f:
        elf = ELFFile(f)
        text_section = elf.get_section_by_name('.text')
        write_memory(0x0000, text_section.data(), size=len(text_section.data()))

def fetch_instruction():
    global pc
    # 取出指令
    inst_bytes = get_memory(pc, 4)
    if (inst_bytes == b'\x00\x00\x00\x00'):
        print("")
        print("End of program")
        sys.exit(0)
    inst = bytes_to_int(inst_bytes)
    print(f"PC: {hex(pc)}  INST: {hex(inst)}")
    opcode = inst & 0x7F
    print(f"Opcode: {hex(opcode)}")
    # 0010011
    if opcode == 0x13:
        i_type = IType(inst)
        print(i_type)
        i_type.execute()
    # 0110011
    if opcode == 0x33:
        funct3, rs1, rs2, rd, funct7 = r_type_decode(inst)
        print(f"Instruction: R-Type, funct3: {funct3}, rs1: {rs1}, rs2: {rs2}, rd: {rd}, funct7: {funct7}")
        match funct3:
            case 0x0:
                print("ADD")
                rs1_value = bytes_to_int(get_reg(rs1))
                rs2_value = bytes_to_int(get_reg(rs2))
                result = rs1_value + rs2_value
                set_reg(rd, result.to_bytes(4, byteorder='little'))
            case _:
                print("Unknown R-Type instruction")
    # 1100011
    if opcode == 0x63:
        imm11, imm4_1, funct3, rs1, rs2, imm10_5, imm12 = b_type_decode(inst)
        print(f"Instruction: B-Type, funct3: {funct3}, rs1: {rs1}, rs2: {rs2}, imm: {imm11}{imm4_1}{imm10_5}{imm12}")
        match funct3:
            case 0x4:
                print("BLT")
                rs1_value = bytes_to_int(get_reg(rs1))
                rs2_value = bytes_to_int(get_reg(rs2))
                offset = (imm12 << 12) | (imm11 << 11) | (imm10_5 << 5) | (imm4_1 << 1)
                
                # 符号扩展
                if offset & (1 << 12):
                    offset = offset - (1 << 13)
                
                if rs1_value < rs2_value:
                    pc += offset
            case _:
                print("Unknown B-Type instruction")
    pc += 4
    
    print_reg()

def print_reg():
    for i in range(32):
        print(f"R{i}: {hex(bytes_to_int(get_reg(i)))}", end=' ')

def r_type_decode(inst: int):
    rd     = (inst >> 7) & 0x1F
    funct3 = (inst >> 12) & 0x7
    rs1    = (inst >> 15) & 0x1F
    rs2    = (inst >> 20) & 0x1F
    funct7 = (inst >> 25) & 0x7F
    return funct3, rs1, rs2, rd, funct7

def b_type_decode(inst: int):
    imm11   = (inst >> 7) & 0x1
    imm4_1  = (inst >> 8) & 0xF
    funct3  = (inst >> 12) & 0x7
    rs1     = (inst >> 15) & 0x1F
    rs2     = (inst >> 20) & 0x1F
    imm10_5 = (inst >> 25) & 0x3F
    imm12   = (inst >> 31) & 0x1
    
    return imm11, imm4_1, funct3, rs1, rs2, imm10_5, imm12

def s_type_decode(inst: int):
    imm4_0  = (inst >> 7) & 0x1F
    funct3  = (inst >> 12) & 0x7
    rs1     = (inst >> 15) & 0x1F
    rs2     = (inst >> 20) & 0x1F
    imm11_5 = (inst >> 25) & 0x7F        

if __name__ == '__main__':
    process_file(sys.argv[1])
    while True:
        fetch_instruction()
