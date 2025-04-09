memory = bytearray(1024)
reg = [b"\x00"] * (32 * 4)
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

def set_reg(reg_num: int, value: bytes):
    global reg
    if reg_num < 0 or reg_num >= len(reg):
        raise ValueError("Register number out of bounds")
    if len(value) != 4:
        raise ValueError("Value must be 4 bytes")
    reg[reg_num] = value

def set_pc(value: int):
    global pc
    pc = value

def get_pc():
    return pc