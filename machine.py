from utils import int_to_bytes, bytes_to_int

memory = bytearray(1024 * 1024)
reg = [b"\x00"] * 32
pc = 0


def write_memory(addr: int, data: bytes, size: int = 4):
    global memory
    if addr < 0 or addr + size >= len(memory):
        raise ValueError("Address out of bounds")
    for i in range(size):
        memory[addr + i] = data[i]


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


def set_reg(reg_num: int, value: int):
    global reg
    if reg_num < 0 or reg_num >= len(reg):
        raise ValueError("Register number out of bounds")
    reg[reg_num] = int_to_bytes(value & 0xFFFFFFFF)


def set_pc(value: int):
    global pc
    pc = value


def get_pc():
    return pc


def print_reg():
    for i in range(32):
        print(f"x{i}: {hex(bytes_to_int(get_reg(i)))}", end=' ')
    # pass
