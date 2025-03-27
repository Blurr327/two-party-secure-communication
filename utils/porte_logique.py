from binary import bit

class PorteLogique :

    def NOT(a : bit, b : bit) -> bit:
        return 1 - a
    
    def XOR(a : bit, b : bit) -> bit:
        return a ^ b
    
    def AND(a : bit, b : bit) -> bit:
        return a & b