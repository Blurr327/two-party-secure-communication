from Crypto.Random.random import getrandbits
from src.circuit.circuit import CircuitCombinatoire
from src.garbled_circuit.ctr import encrypt_ctr
from src.circuit.node import Node
from src.circuit.etiquette import Etiquette

def generate_wire_labels(circuit : CircuitCombinatoire):
    wire_labels = {}
    for node in circuit.nodes:
        if node.get_etiquette() in {Etiquette.OUTa, Etiquette.OUTb}:
            wire_labels[node] = (0, 1)
            continue
        randbit = getrandbits(1)
        label0_missing_1_bit = getrandbits(127)
        label1_missing_1_bit = getrandbits(127)
        wire_labels[node] = ((label0_missing_1_bit << 1) | randbit, (label1_missing_1_bit << 1) | (1-randbit))
    return wire_labels

def get_index_from_input_labels(label_input_list):
    result = 0
    for label, i in zip(label_input_list, range(len(label_input_list))):
        result |= ((label & 1) << i)
    return result

def encrypt_output_label_with_input_labels(label_input_list, output_label, nonce):
    current_message = output_label
    for label in label_input_list:
        current_message = encrypt_ctr(label, current_message, nonce)
    return current_message

def decrypt_encrypted_output_label_with_input_labels(label_input_list, encrypted_output_label, nonce):
    return encrypt_output_label_with_input_labels(label_input_list[::-1], encrypted_output_label, nonce)

def binary_to_label_list(binary_list, label_tuples):
    return [label_tuples[index][binary_list[index]] for index in range(len(binary_list))]

def get_input_possibilities(node : Node):
    result = []
    node_type = node.get_etiquette()
    if node_type in {Etiquette.AND, Etiquette.XOR}:
        result = [[0, 0], [0, 1], [1, 0], [1, 1]]
    elif node_type in {Etiquette.NOT, Etiquette.OUTa, Etiquette.OUTb}:
        result = [[0], [1]]
    return result

def garble(circuit : CircuitCombinatoire, wire_labels, nonce):
    garbled_circuit_tables = {}

    for node in circuit.topo_order:
        node_type = node.get_etiquette()
        if node_type in {Etiquette.INa, Etiquette.INb}:
            continue
        input_nodes = circuit.reverse_edges[node]
        input_label_tuples = [wire_labels[input_node] for input_node in input_nodes]
        input_possibilities = get_input_possibilities(node)
        garbled_circuit_tables[node] = [0 for _ in range(len(input_possibilities))]
        for input_possibility in input_possibilities:
            input_labels = binary_to_label_list(input_possibility, input_label_tuples)

            output = node_type.execute(*input_possibility)
            output_label = wire_labels[node][output]

            encrypted_output = encrypt_output_label_with_input_labels(input_labels, output_label, nonce)

            output_index = get_index_from_input_labels(input_labels)
            garbled_circuit_tables[node][output_index] = encrypted_output
    return garbled_circuit_tables

def evaluate(circuit : CircuitCombinatoire, garbled_circuit_tables, wire_values, nonce):
    for node in circuit.topo_order:
        if node in wire_values:
            continue
        input_nodes = circuit.reverse_edges[node]
        input_labels = [wire_values[input_node] for input_node in input_nodes]
        index = get_index_from_input_labels(input_labels)
        encrypted_output_label = garbled_circuit_tables[node][index]
        output_label = decrypt_encrypted_output_label_with_input_labels(input_labels, encrypted_output_label, nonce)
        wire_values[node] = output_label
    return ([wire_values[node[0]] for node in circuit.nodes_output], [wire_values[node[1]] for node in circuit.nodes_output])
