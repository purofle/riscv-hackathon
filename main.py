import sys

from elftools.elf.elffile import ELFFile

from instruction.b_type import BType
from instruction.i_type import IType
from instruction.r_type import RType
from instruction.u_type import UType
from machine import get_memory, get_reg, write_memory, get_pc, set_pc
from utils import bytes_to_int


def process_file(filename):
    print('Processing file:', filename)
    with open(filename, 'rb') as f:
        elf = ELFFile(f)
        text_section = elf.get_section_by_name('.text')
        write_memory(0x0000, text_section.data(), size=len(text_section.data()))

def fetch_instruction():
    # 取出指令
    inst_bytes = get_memory(get_pc(), 4)
    if inst_bytes == b'\x00\x00\x00\x00':
        print("")
        print("End of program")
        sys.exit(0)
    inst = bytes_to_int(inst_bytes)
    print(f"PC: {hex(get_pc())}  INST: {hex(inst)}")
    opcode = inst & 0x7F
    if opcode == 0b0010011:
        i_type = IType(inst)
        print(i_type)
        i_type.execute()

    if opcode == 0b0110011:
        r_type = RType(inst)
        print(r_type)
        r_type.execute()

    if opcode == 0b1100011:
        b_type = BType(inst)
        print(b_type)
        b_type.execute()

    if opcode == 0b0110111:
        u_type = UType(inst)
        print(u_type)
        u_type.lui()

    set_pc(get_pc() + 4)
    print_reg()

def print_reg():
    for i in range(32):
        print(f"R{i}: {hex(bytes_to_int(get_reg(i)))}", end=' ')

if __name__ == '__main__':
    process_file(sys.argv[1])
    while True:
        fetch_instruction()
