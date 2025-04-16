from __future__ import annotations
from circuit.node import Node
from graphviz import Digraph
from circuit.etiquette import Etiquette
from collections import defaultdict
from utils.binary import BinaryList

class CircuitCombinatoire:
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    nodes : list[Node]
    edges : dict[Node, list[Node]]
    reverse_edges : dict[Node, list[Node]]
    nodes_input : list[tuple[Node, Node]]
    nodes_output : list[tuple[Node, Node]]

    def __init__(self):
        self.nodes = []
        self.edges = defaultdict(list)
        self.nodes_input = []
        self.nodes_output = []
        self.topo_order = []
    
    def add_edge(self, src: Node, dst: Node):
        self.edges[src].append(dst)

    def verify_circuit(self) -> bool:
        for node in self.nodes:
            outdeg = node.get_outdeg(self.edges)
            indeg = node.get_indeg(self.edges)

            etiquette = node.get_etiquette()

            if indeg != etiquette.get_indeg():
                return False

            match etiquette:
                case s if s in {Etiquette.INa, Etiquette.INb}:
                    if outdeg < 1:
                        return False
                case s if s == Etiquette.NOT:
                    if outdeg < 1:
                        return False
                case s if s in {Etiquette.XOR, Etiquette.AND}:
                    if outdeg < 1:
                        return False
                case s if s in {Etiquette.OUTa, Etiquette.OUTb}:
                    if outdeg != 0:
                        return False
                    
        return True
    
    def visualize(self) -> None:
        """ Visualize the circuit using graphviz.
        """
        
        dot = Digraph()

        for node in self.nodes:
            label = node.get_etiquette().name 
            if node.get_output() is not None:
                label += f" : {node.get_output()}"
            dot.node(str(id(node)), label)

        for src, dsts in self.edges.items():
            for dst in dsts:
                dot.edge(str(id(src)), str(id(dst)))

        # Create subgraph for input nodes so that they are on the same rank and in the correct order
        with dot.subgraph() as s:
            s.attr(rank='same')
            for in_node in self.nodes_input :
                s.node(str(id(in_node[0])))
                s.node(str(id(in_node[1])))

            for i in range(len(self.nodes_input) - 1):
                s.edge(str(id(self.nodes_input[i][0])), str(id(self.nodes_input[i+1][0])), style='invis')
                s.edge(str(id(self.nodes_input[i][1])), str(id(self.nodes_input[i+1][1])), style='invis')

        # Create subgraph for output nodes so that they are on the same rank and in the correct order
        with dot.subgraph() as s:
            s.attr(rank='same')
            for out_node in self.nodes_output :
                s.node(str(id(out_node[0])))
                s.node(str(id(out_node[1])))

            for i in range(len(self.nodes_output) - 1):
                s.edge(str(id(self.nodes_output[i][0])), str(id(self.nodes_output[i+1][0])), style='invis')
                s.edge(str(id(self.nodes_output[i][1])), str(id(self.nodes_output[i+1][1])), style='invis')

        dot.render('circuit_graph', view=True, format='png')

    def create_or(self, node_1 : Node, node_2 : Node) -> Node:
        """ Create a OR circuit with two inputs. OR = XOR(AND(node_1, node_2), NOT(node_1))
        The circuit will have 2 inputs and 1 output.
        """
        # Create nodes for OR operation
        node_xor_all = Node(Etiquette.XOR)
        node_and = Node(Etiquette.AND)
        node_xor = Node(Etiquette.XOR)
        self.nodes.extend([node_xor_all, node_and, node_xor])

        # Create edges for OR operation
        self.add_edge(node_1, node_and)
        self.add_edge(node_2, node_and)

        self.add_edge(node_1, node_xor)
        self.add_edge(node_2, node_xor)

        self.add_edge(node_and, node_xor_all)
        self.add_edge(node_xor, node_xor_all)

        # Return the output node
        return node_xor_all
    
    def compute_reverse_edges(self) -> dict:
        """ Compute the reverse edges of the circuit """
   
        self.reverse_edges = {node: [] for node in self.nodes}

        for src in self.edges:
            for dest in self.edges[src]:
                self.reverse_edges[dest].append(src)

        return self.reverse_edges
    
    def compute_topological_order(self) -> list[Node]:
        """Return a topological order of the node"""

        # Number of edges for each node
        in_degree = {node: 0 for node in self.nodes}
        for source_node in self.edges:
            for target_node in self.edges[source_node]:
                in_degree[target_node] += 1

        # Initialize the queue with nodes that have no incoming edges
        queue = [node for node in self.nodes if in_degree[node] == 0]

        topo_order = []

        while queue:
            node = queue.pop(0)
            topo_order.append(node)

            for neighbor in self.edges.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return topo_order
    
    def run_circuit(self, in_a_values : BinaryList, in_b_values : BinaryList) -> tuple[BinaryList, BinaryList]:
        """ Execute the circuit with values for in a and b
        
        Keyword arguments:
        in_a -- value for a
        in_b -- value for b
        Return: the result of the circuit
        """
        if len(self.reverse_edges) == 0 :
            self.compute_reverse_edges()

        # Reset output and inputs values
        self.reset()

        assert len(in_a_values) == len(self.nodes_input), "Input length does not match the number of inputs in the circuit"
        assert len(in_b_values) == len(self.nodes_input), "Input length does not match the number of inputs in the circuit"

        if len(self.topo_order) == 0 :
            self.topo_order = self.compute_topological_order()

        final_nodes : list[Node] = []

        # Put the values in the circuit
        for node_a, node_b in self.nodes_input:
            node_a.set_output(in_a_values.pop(0))
            node_b.set_output(in_b_values.pop(0))

        # Process the circuit
        for node in self.topo_order :

            if node.get_output() is None:
                inputs = [node_before.get_output() for node_before in self.reverse_edges[node]]
                output = node.get_etiquette().execute(*inputs)
                node.set_output(output)

                if node.get_etiquette() == Etiquette.OUTa or node.get_etiquette() == Etiquette.OUTb :

                    final_nodes.append(node)

        return ([node[0].get_output() for node in self.nodes_output], [node[1].get_output() for node in self.nodes_output])

    def reset(self) :
        for node in self.nodes :
            node.reset()
        


