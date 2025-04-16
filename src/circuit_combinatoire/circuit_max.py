from circuit.circuit import CircuitCombinatoire
from circuit.node import Node
from circuit.etiquette import Etiquette

class CircuitMax(CircuitCombinatoire) :
    def __init__(self, n : int):
        """ Create a max circuit with n inputs.
        """
        super().__init__()
        self.create_max(n)
        assert self.verify_circuit(), "The circuit is not valid"
        self.compute_reverse_edges()
        self.topo_order = self.compute_topological_order()

    def create_is_a_max(self, n : int, current : int = 0, previous_node : Node = None, equal_nodes : list[Node] = []) -> Node :
        """ 
            Create a is a > b circuit with n inputs.

            Keyword arguments:
            n -- number of inputs
            current -- current level
            previous_node -- previous node
            equal_nodes -- list of equal nodes

            Return: the last node of the circuit
        """
        if current == n:
            return previous_node
        else:
            # (A0 > B0) | (A0 == B0) & (A1 > B1) | (A1 == B1) & ... & (An > Bn)

            # Create nodes for the current level (A > B)
            node_a = Node(Etiquette.INa)
            node_b = Node(Etiquette.INb)
            # Add nodes to nodes_input
            self.nodes_input.append((node_a, node_b))

            node_and = Node(Etiquette.AND)
            node_not = Node(Etiquette.NOT)

            # Add nodes to the circuit
            self.nodes.extend([node_a, node_b, node_and, node_not])

            # Create edges for the current level
            self.add_edge(node_a, node_and)
            self.add_edge(node_b, node_not)
            self.add_edge(node_not, node_and)

            # Create equal nodes (A == B)
            for node in equal_nodes:
                node_and_equal = Node(Etiquette.AND)
                self.nodes.append(node_and_equal)
                self.add_edge(node_and, node_and_equal)
                self.add_edge(node, node_and_equal)
                node_and = node_and_equal
                

            # create egality nodes for current level
            if (current < n -1 ) :
                node_egal_xor = Node(Etiquette.XOR)
                node_egal_not = Node(Etiquette.NOT)
                self.nodes.extend([node_egal_xor, node_egal_not])
                self.add_edge(node_a, node_egal_xor)
                self.add_edge(node_b, node_egal_xor)
                self.add_edge(node_egal_xor, node_egal_not)
                equal_nodes.append(node_egal_not)

            # Connect to the previous level
            if previous_node is not None:        
                node_xor_or = self.create_or(previous_node, node_and)
                previous_node = node_xor_or
            else:
                # First 
                previous_node = node_and



            # Create the next level
            return self.create_is_a_max(n, current + 1, previous_node, equal_nodes)

    def create_max(self, n : int):
        """ Create a max circuit with n inputs.
        The circuit will have 2n inputs and 2n outputs.
        
        Keyword arguments:
        n -- number of inputs
        """
        
        node_is_a_max = self.create_is_a_max(n)
        print(node_is_a_max)

        for node_a, node_b in self.nodes_input:
            # Outputn = (Inan & aMax | Inbn & ¬aMax)
            node_and_a = Node(Etiquette.AND)
            node_and_b = Node(Etiquette.AND)
            node_not = Node(Etiquette.NOT)

            #  Inan & aMax
            self.nodes.extend([node_and_a, node_and_b, node_not])


            self.add_edge(node_a, node_and_a)
            self.add_edge(node_is_a_max, node_and_a)



            #  Inbn & ¬aMax
            self.add_edge(node_is_a_max, node_not)
            self.add_edge(node_not, node_and_b)
            self.add_edge(node_b, node_and_b)


            # nodes or
            node_or = self.create_or(node_and_a, node_and_b)

            # Create output nodes
            node_out_a = Node(Etiquette.OUTa)
            node_out_b = Node(Etiquette.OUTb)
            self.nodes.extend([node_out_a, node_out_b])
            self.nodes_output.append((node_out_a, node_out_b))

            # Connect to the output nodes
            self.add_edge(node_or, node_out_a)    
            self.add_edge(node_or, node_out_b)


        # Verify the circuit
        if not self.verify_circuit():
            raise ValueError("The circuit is not valid")

        # Return the output nodes
        return [node_out_a, node_out_b]

            
