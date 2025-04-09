import sys
import struct
from elftools.elf.elffile import ELFFile

memory = bytearray(1024)
reg = [b"\x00"] * (32 * 4)
pc = 0

def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder='little')

def write_memory(aadr: int, data: bytes, size: int = 4):
    global memory
    if aadr < 0 or aadr + size >= len(memory):
        raise ValueError("Address out of bounds")
    for i in range(size):
        memory[aadr + i] = data[i]

def get_memory(addr: int, size: int):
    global memory
    if addr < 0 or addr + size >= len(memory):
        raise ValueError("Address out of bounds")
    return memory[addr:addr + size]

def get_reg(reg_num: int):
    global reg
    if reg_num < 0 or reg_num >= len(reg):
        raise ValueError("Register number out of bounds")
    return reg[reg_num]

def set_reg(reg_num: int, value: bytes):
    global reg
    if reg_num < 0 or reg_num >= len(reg):
        raise ValueError("Register number out of bounds")
    if len(value) != 4:
        raise ValueError("Value must be 4 bytes")
    reg[reg_num] = value

def process_file(filename):
    print('Processing file:', filename)
    with open(filename, 'rb') as f:
        elf = ELFFile(f)
        text_section = elf.get_section_by_name('.text')
        write_memory(0x0000, text_section.data(), size=len(text_section.data()))

def fetch_instruction():
    global pc
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
        funct3, rs1, rd, imm = i_type_decode(inst)
        print(f"Instruction: I-Type, funct3: {funct3}, rs1: {rs1}, rd: {rd}, imm: {imm}")
        match funct3:
            case 0x0:
                print("ADDI")
                rs1_value = bytes_to_int(get_reg(rs1))
                result = rs1_value + imm
                set_reg(rd, result.to_bytes(4, byteorder='little'))
            case _:
                print("Unknown I-Type instruction")
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

def i_type_decode(inst: int):
    rd     = (inst >> 7) & 0x1F
    funct3 = (inst >> 12) & 0x7
    rs1    = (inst >> 15) & 0x1F
    imm    = (inst >> 20) & 0xFFF
    return funct3, rs1, rd, imm

def r_type_decode(inst: int):
    rd = (inst >> 7) & 0x1F
    funct3 = (inst >> 12) & 0x7
    rs1 = (inst >> 15) & 0x1F
    rs2 = (inst >> 20) & 0x1F
    funct7 = (inst >> 25) & 0x7F
    return funct3, rs1, rs2, rd, funct7

def b_type_decode(inst: int):
    imm11 = (inst >> 7) & 0x1
    imm4_1 = (inst >> 8) & 0xF
    funct3 = (inst >> 12) & 0x7
    rs1 = (inst >> 15) & 0x1F
    rs2 = (inst >> 20) & 0x1F
    imm10_5 = (inst >> 25) & 0x3F
    imm12 = (inst >> 31) & 0x1
    
    return imm11, imm4_1, funct3, rs1, rs2, imm10_5, imm12

if __name__ == '__main__':
    process_file(sys.argv[1])
    while True:
        fetch_instruction()
