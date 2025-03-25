# TODO : Ajouter des tests unitaires
from typing import Literal, List, TypeAlias

Bit: TypeAlias = Literal[0, 1]
BinaryList: TypeAlias = List[Bit]

def to_int(binary: BinaryList) -> int: 
    return int("".join(str(bit) for bit in binary), 2)

def max(a: BinaryList, b: BinaryList) -> BinaryList:
    if len(a) != len(b):
        raise ValueError("Both lists must have the same length")
    if to_int(a) > to_int(b):
        return a
    return b