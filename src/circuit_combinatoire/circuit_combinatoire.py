from __future__ import annotations
from enum import Enum
from node import Node
from graphviz import Digraph

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
        from graphviz import Digraph
        dot = Digraph()

        for node in self.nodes:
            label = ','.join([et.name for et in node.get_value()])
            dot.node(str(id(node)), label)

        for src, dst in self.edges:
            dot.edge(str(id(src)), str(id(dst)))

        dot.render('circuit_graph', view=True, format='png')

    def create_or(self, node_1 : Node, node_2 : Node) -> Node:
        # Create nodes for OR operation
        node_not = Node({Etiquette.NOT})
        node_and = Node({Etiquette.AND})
        node_xor = Node({Etiquette.XOR})
        self.nodes.extend([node_not, node_and, node_xor])

        # Create edges for OR operation
        self.edges.append((node_1, node_and))
        self.edges.append((node_2, node_and))
        self.edges.append((node_1, node_not))
        self.edges.append((node_and, node_xor))
        self.edges.append((node_not, node_xor))

        # Return the output node
        return node_xor
    
    def create_is_a_max(self, n : int, current : int = 0, previous_node : Node = None, equal_nodes : list[Node] = []) -> Node :
        if current == n:
            return previous_node
        else:
            # Create nodes for the current level
            node_a = Node({Etiquette.INa})
            node_b = Node({Etiquette.Inb})
            node_and = Node({Etiquette.AND})
            node_not = Node({Etiquette.NOT})

            # Add nodes to the circuit
            self.nodes.extend([node_a, node_b, node_and, node_not])

            # Create edges for the current level
            self.edges.append((node_a, node_and))
            self.edges.append((node_b, node_not))
            self.edges.append((node_not, node_and))

            for node in equal_nodes:
                node_and_equal = Node({Etiquette.AND})
                self.nodes.append(node_and_equal)
                self.edges.append((node_and, node_and_equal))
                self.edges.append((node, node_and_equal))
                node_and = node_and_equal
                

            # create egality nodes
            node_egal_xor = Node({Etiquette.XOR})
            node_egal_not = Node({Etiquette.NOT})
            self.nodes.extend([node_egal_xor, node_egal_not])
            self.edges.append((node_a, node_egal_xor))
            self.edges.append((node_b, node_egal_xor))
            self.edges.append((node_egal_xor, node_egal_not))
            equal_nodes.append(node_egal_not)

            # Connect to the previous level
            if previous_node is not None:        
                node_xor_or = self.create_or(previous_node, node_and)
                previous_node = node_xor_or
            else:
                previous_node = node_and

            self.visualize()

            # Create the next level
            self.create_is_a_max(n, current + 1, previous_node, equal_nodes)

    def create_max(self, n : int):
        """ Create a max circuit with n inputs.
        The circuit will have 2n inputs and 2n outputs.
        
        Keyword arguments:
        n -- number of inputs
        """
        
        node_is_a_max = self.create_is_a_max(n)

        nodes_input = [node for node in self.nodes if Etiquette.INa or Etiquette.INb in node.get_value()]

        for node in nodes_input:
            # Outputn = Inan | ¬Inbn 
            node_and_a = Node({Etiquette.AND})
            node_and_b = Node({Etiquette.AND})
            node_not = Node({Etiquette.NOT})

            


if __name__ == "__main__":
    circuit = CircuitCombinatoire(3)
    circuit.create_is_a_max(2)
    circuit.visualize()
            
