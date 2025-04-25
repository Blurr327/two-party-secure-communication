import pytest
import time
from transfert_inconscient.ot_protocol import ot_protocol
from transfert_inconscient.elGamal import generate_keys, encrypt, decrypt
from transfert_inconscient.log_discret import calcul_log_discret
import random

rdm = random.SystemRandom()

"""
def test_ot_protocol():
    
    Test du protocole OT pour vérifier qu'il fonctionne correctement
    avec une taille de clé de 10 bits.
    
    print("\n==== DÉBUT DU PROTOCOLE OT ====")
    
    # Lance le protocole OT
    ot_protocol(10)
    
    print("\n==== FIN DU PROTOCOLE OT ====")
"""

#on effectue plusieurs tests pour un nnombre de bits différents 
@pytest.mark.parametrize("bits", [8, 12, 16, 20])
def test_log_discret_resistance(bits):
    
    """
    Vérifie qu'il n'est pas possible (ou pas facile) de retrouver la clé privée a
    à partir de la clé publique (p, g, A) par attaque du logarithme discret.
    """
    
    public_key, private_key = generate_keys(bits)
    p, g, A = public_key
    _, a = private_key

    # On tente de retrouver a tel que g^a ≡ A (mod p)
    start = time.time()
    result = calcul_log_discret(g, A, p)
    end = time.time()

    elapsed = end - start

    if bits <= 16:
        # Sur de petites tailles, c'est normal que ça réussisse
        assert result == a, f"[OK] L'attaque réussit à petite taille ({bits} bits)"
    else:
        # Sur > 16 bits, on attend que ça soit long ou que ça échoue
        assert result != a or elapsed > 2, \
            f"[ÉCHEC] Le log discret a réussi trop vite ({elapsed:.3f}s) sur {bits} bits !"
