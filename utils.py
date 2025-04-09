def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder='little')

def int_to_bytes(i: int) -> bytes:
    return i.to_bytes(4, byteorder='little')