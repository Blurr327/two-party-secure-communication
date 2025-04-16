from enum import Enum
from utils.binary import Bit

class Etiquette(Enum):
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    INa = 1
    INb = 2
    NOT = 3
    XOR = 4
    AND = 5
    OUTa = 6
    OUTb = 7

    def get_indeg(self) -> int:
        match self :
            case s if s in {Etiquette.INa, Etiquette.INb}:
                return 0
            case s if s == Etiquette.NOT:
                return 1
            case s if s in {Etiquette.XOR, Etiquette.AND}:
                return 2
            case s if s in {Etiquette.OUTa, Etiquette.OUTb}:
                return 1
            
    def execute(self, a : Bit, b : Bit = None) :
        match self : 
            case s if s == Etiquette.NOT:
                return 1 - a
            case s if s == Etiquette.XOR:
                return a ^ b
            case s if s == Etiquette.AND:
                return a & b
            case s if s in {Etiquette.OUTa, Etiquette.OUTb, Etiquette.INa, Etiquette.INb}:
                return a
        

        