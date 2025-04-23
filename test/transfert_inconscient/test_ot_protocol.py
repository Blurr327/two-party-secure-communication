from transfert_inconscient.ot_protocol import ot_protocol
from transfert_inconscient.elGamal import generate_keys, encrypt, decrypt
import random

rdm = random.SystemRandom()

def test_ot_protocol():
    """
    Test du protocole OT pour vérifier qu'il fonctionne correctement
    avec une taille de clé de 10 bits.
    """
    print("\n==== DÉBUT DU PROTOCOLE OT ====")
    
    # Lance le protocole OT
    ot_protocol(10)
    
    print("\n==== FIN DU PROTOCOLE OT ====")
