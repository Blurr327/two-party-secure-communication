import pytest
from src.circuit_combinatoire.circuit_max import CircuitMax
from src.utils.binary import max


def test_max():
    """ Test the max function.
    """
    a = [1, 0, 1, 0]
    b = [0, 1, 0, 1]
    assert max(a, b) == a

    a = [0, 0, 0, 0]
    b = [1, 1, 1, 1]
    assert max(a, b) == b

    a = [1, 1, 1, 1]
    b = [1, 1, 1, 1]
    assert max(a, b) == a

    a = [0]
    b = [0]
    assert max(a, b) == a

def test_circuit_max() :
    """ Test the circuit max8 """
    circuit = CircuitMax(8)

    # Test the circuit with all the inputs possible
    for i in range(256) :
        for j in range(256) :

            a = [(i >> k) & 1 for k in range(8)]
            b = [(j >> k) & 1 for k in range(8)]

            a_copy = a.copy()
            b_copy = b.copy()

            out_a, out_b = circuit.run_circuit(a, b)

            assert out_a == max(a_copy, b_copy), f"Output A is not correct :  {out_a} != {max(a_copy, b_copy)}"
            assert out_b == max(a_copy, b_copy), f"Output B is not correct : {out_b} != {max(a_copy, b_copy)}"

if __name__ == "__main__":
    pytest.main()
