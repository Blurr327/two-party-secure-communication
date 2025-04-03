from __future__ import annotations
from src.circuit.node import Node
from graphviz import Digraph
from src.circuit.etiquette import Etiquette
from collections import defaultdict

class CircuitCombinatoire:
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    nodes : list[Node]
    edges : dict[Node, list[Node]]


    def __init__(self):
        self.nodes = []
        self.edges = defaultdict(list)
        self.nodes_input = []

    def get_etiquettes(self, node : Node) -> set[Etiquette]:
        return node.get_value()
    
    def add_edge(self, src: Node, dst: Node):
        self.edges[src].append(dst)

    def verify_circuit(self) -> bool:
        for node in self.nodes:
            outdeg = node.get_outdeg(self.edges)
            indeg = node.get_indeg(self.edges)

            etiquettes = self.get_etiquettes(node)

            match etiquettes:
                case s if s == {Etiquette.INa, Etiquette.INb}:
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
        """ Visualize the circuit using graphviz.
        """
        
        dot = Digraph()

        for node in self.nodes:
            label = ','.join([et.name for et in node.get_value()])
            dot.node(str(id(node)), label)

        for src, dsts in self.edges.items():
            for dst in dsts:
                dot.edge(str(id(src)), str(id(dst)))

        dot.render('circuit_graph', view=True, format='png')

    def create_or(self, node_1 : Node, node_2 : Node) -> Node:
        """ Create a OR circuit with two inputs. OR = XOR(AND(node_1, node_2), NOT(node_1))
        The circuit will have 2 inputs and 1 output.
        """
        # Create nodes for OR operation
        node_not = Node({Etiquette.NOT})
        node_and = Node({Etiquette.AND})
        node_xor = Node({Etiquette.XOR})
        self.nodes.extend([node_not, node_and, node_xor])

        # Create edges for OR operation
        self.add_edge(node_1, node_and)
        self.add_edge(node_2, node_and)
        self.add_edge(node_1, node_not)
        self.add_edge(node_and, node_xor)
        self.add_edge(node_not, node_xor)

        # Return the output node
        return node_xor

