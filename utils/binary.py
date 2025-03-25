from typing import Literal, List, TypeAlias

Bit: TypeAlias = Literal[0, 1]
BinaryList: TypeAlias = List[Bit]

def max(a: BinaryList, b: BinaryList) -> BinaryList:
    if len(a) != len(b):
        raise ValueError("Both lists must have the same length")
    
def to_int(binary: BinaryList) -> int:
    return int("".join(str(bit) for bit in binary), 2)