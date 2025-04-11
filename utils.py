def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder='little')

def int_to_bytes(i: int) -> bytes:
    return i.to_bytes(4, byteorder='little')

def sign_extend(value: int, bits: int) -> int:
    if value & (1 << (bits - 1)):
        value -= 1 << bits
    return value