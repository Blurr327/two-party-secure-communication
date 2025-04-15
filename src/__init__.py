from circuit_combinatoire.circuit_max import CircuitMax

if __name__ == "__main__":
    # Create a circuit with 3 inputs
    circuit = CircuitMax(8)
    
    in_a, in_b = circuit.run_circuit([0, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1])
    circuit.visualize()

    print("Output A: ", in_a)
    print("Output B: ", in_b)