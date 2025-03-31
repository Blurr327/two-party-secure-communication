from enum import Enum
from circuit_combinatoire.node import Node
from __future__ import annotations


class Etiquette(Enum):
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    INa = 1
    Inb = 2
    NOT = 3
    XOR = 4
    AND = 5
    OUTa = 6
    OUTb = 7

class CircuitCombinatoire:
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    nodes : list[Node]
    edges : list[tuple[Node, Node]]

    def __init__(self, n : int):
        self.nodes = []
        self.edges = []
        
        input_a = Node({Etiquette.INa})
        input_b = Node({Etiquette.Inb})

        self.nodes.extend(input_a, input_b)

    def get_etiquettes(self, node : Node) -> set[Etiquette]:
        return node.get_value()

    def verify_circuit(self) -> bool:
        for node in self.nodes:
            indeg = node.get_indeg(self.edges)
            outdeg = node.get_outdeg(self.edges)

            etiquettes = self.get_etiquettes(node)

            match etiquettes:
                case s if s == {Etiquette.INa, Etiquette.Inb}:
                    if indeg != 0:
                        return False
                    if outdeg < 1:
                        return False
                case s if s == {Etiquette.NOT}:
                    if indeg != 1:
                        return False
                    if outdeg < 1:
                        return False
                case s if s == {Etiquette.XOR, Etiquette.AND}:
                    if indeg != 2:
                        return False
                    if outdeg < 1:
                        return False
                case s if s == {Etiquette.OUTa, Etiquette.OUTb}:
                    if indeg != 1:
                        return False
                    if outdeg != 0:
                        return False
                    
        return True
    
    def visualize(self) -> None:
        pass
    
    def create_is_a_max(self, n : int, current : int = 1) :
        if current == n:
            pass
        else:
            node_a = Node({Etiquette.INa})
            node_b = Node({Etiquette.Inb})

            
