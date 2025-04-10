#!/usr/bin/env python3

import sys

from elftools.elf.elffile import ELFFile

from instruction.b_type import BType
from instruction.i_type import IType
from instruction.r_type import RType
from instruction.s_type import SType
from instruction.u_type import UType
from machine import get_memory, write_memory, get_pc, set_pc, print_reg
from utils import bytes_to_int


def process_file(filename):
    print('Processing file:', filename)
    with open(filename, 'rb') as f:
        elf = ELFFile(f)
        addr = 0
        for i in elf.iter_segments("PT_LOAD"):
            print("Loading segment:", i.header)
            write_memory(i.header["p_paddr"], i.data(), len(i.data()))

    entry = elf.header["e_entry"]
    set_pc(entry)

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

    match opcode:
        case 0b0010011 | 0b1110011:
            i_type = IType(inst)
            print(i_type)
            i_type.execute()
        case 0b0110011:
            r_type = RType(inst)
            print(r_type)
            r_type.execute()
        case 0b1100011:
            b_type = BType(inst)
            print(b_type)
            b_type.execute()
        case 0b0110111:
            u_type = UType(inst)
            print(u_type)
            u_type.lui()
        case 0b0100011:
            s_type = SType(inst)
            print(s_type)
            s_type.execute()
        case 0b1111:
            # fence
            pass

        case _:
            print(f"Unknown instruction with opcode: {bin(opcode)}")
            sys.exit(1)


    set_pc(get_pc() + 4)
    print_reg()

if __name__ == '__main__':
    process_file(sys.argv[1])
    while True:
        fetch_instruction()
