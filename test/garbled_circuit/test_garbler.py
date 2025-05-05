from src.garbled_circuit.garbler import *
from src.circuit.circuit import CircuitCombinatoire
from src.circuit.etiquette import Etiquette
from src.circuit.node import Node
from src.circuit_combinatoire.circuit_max import CircuitMax
from Crypto.Random.random import getrandbits


def create_simple_circuit():
  circuit = CircuitCombinatoire()
  in_a = Node(Etiquette.INa)
  in_b = Node(Etiquette.INb)
  circuit.nodes_input.append((in_a, in_b))

  and_gate = Node(Etiquette.AND)
  out_a = Node(Etiquette.OUTa)
  out_b = Node(Etiquette.OUTb)
  circuit.nodes_output.append((out_a, out_b))
  circuit.nodes.extend([in_a, in_b, and_gate, out_a, out_b])
  circuit.add_edge(in_a, and_gate)
  circuit.add_edge(in_b, and_gate)
  circuit.add_edge(and_gate, out_a)
  circuit.add_edge(and_gate, out_b)

  circuit.reverse_edges = circuit.compute_reverse_edges()
  circuit.topo_order = circuit.compute_topological_order()
  return circuit

def test_create_simple_and_circuit():
  circuit = create_simple_circuit()

  out1, out2 = circuit.run_circuit([1], [1])
  assert out1 == [1]
  assert out2 == out1

  out1, out2 = circuit.run_circuit([1], [0])
  assert out1 == [0]
  assert out2 == out1

def test_label_generation():
  labels_dict = {}
  circuit = create_simple_circuit()
  wire_labels = generate_wire_labels(circuit)
  for node in circuit.nodes:
    label0 = wire_labels[node][0]
    label1 = wire_labels[node][1]
    if node.get_etiquette() in {Etiquette.OUTa, Etiquette.OUTb}:
      assert label0 == 0 and label1 == 1
      continue
    assert label1.bit_length() <= 128 and label0.bit_length() <= 128
    assert not ((label0 in labels_dict) or (label1 in labels_dict)) # make sure there are no repeating labels
    labels_dict[label0] = 1
    labels_dict[label1] = 1
    assert (label0 & 1) ^ (label1 & 1) # make sure that one label has a 1 at the other has a 0 at the end

def test_label_encryption_decryption():
  input_labels = [getrandbits(128) for i in range(5)]
  output_label = getrandbits(128)
  encrypted_output_label = encrypt_output_label_with_input_labels(input_labels, output_label, 0)
  decrypted = decrypt_encrypted_output_label_with_input_labels(input_labels, encrypted_output_label, 0)
  assert output_label == decrypted

def test_index_calculation():
  input_labels = [0, 13310, 138301] # index should be 100
  index = get_index_from_input_labels(input_labels)
  assert index == 4

def test_binary_to_label_list():
  binary_list = [0, 0, 1]
  label_tuples = [(1, 0), (1, 0), (0, 1)]
  assert binary_to_label_list(binary_list, label_tuples) == [1, 1, 1]

def test_garble_evaluate():
  circuit = create_simple_circuit()
  wire_labels = generate_wire_labels(circuit)
  tables = garble(circuit, wire_labels, 0)
  wire_values = {}
  for nodea, nodeb in circuit.nodes_input:
    wire_values[nodea] = wire_labels[nodea][1]
    wire_values[nodeb] = wire_labels[nodeb][1]
  resa, resb = evaluate(circuit, tables, wire_values, 0)
  assert resa == [1]
  assert resb == [1]

def test_garble_evaluate_on_max_circuit():
  circuit = CircuitMax(4)
  wire_labels = generate_wire_labels(circuit)
  tables = garble(circuit, wire_labels, 0)
  input_a = [1, 0, 1, 0]
  input_b = [1, 1, 0, 0]
  wire_values = {}
  for i in range(len(circuit.nodes_input)):
    nodea, nodeb = circuit.nodes_input[i]
    wire_values[nodea] = wire_labels[nodea][input_a[i]]
    wire_values[nodeb] = wire_labels[nodeb][input_b[i]]
  resa, resb = evaluate(circuit, tables, wire_values, 0)
  assert resa == [1, 1, 0, 0]
  assert resb == [1, 1, 0, 0]

