import pytest
import time
from transfert_inconscient.ot_protocol import ot_protocol
from transfert_inconscient.elGamal import generate_keys
from transfert_inconscient.log_discret import calcul_log_discret

# Multiprocessing permet de créer des processus séparés et donc d'arrêter directement au bout de 30 secondes
from multiprocessing import Process, Queue

@pytest.mark.parametrize("bits", [16, 50, 128])
def test_ot_protocol(bits):
    """ Verifie le bon fonctionnement du protocole OT pour un nombre de bits donné.
    """
    
    
    print("\n==== DÉBUT DU PROTOCOLE OT ====")
        
    m0, m1, b, m_decoded = ot_protocol(bits)

    print(f"m0 = {m0}, m1 = {m1}, b = {b}, m_decoded = {m_decoded}")

    # Vérification que le message déchiffré est le même que celui d'origine
    assert m_decoded == (m0 if b == 0 else m1), \
        f"Erreur : message déchiffré {m_decoded} n'est pas égal au message original {m0 if b == 0 else m1}"
    # Vérification que le message déchiffré est bien l'un des deux messages
    assert m_decoded in (m0, m1), \
        f"Erreur : message déchiffré {m_decoded} n'est pas égal à m0 {m0} ou m1 {m1}"
    
    
    print("\n==== FIN DU PROTOCOLE OT ====")

def attaque(bits, queue):
    """
    Fonction pour tester l'algorithme ElGamal en générant les clés,
    en chiffrant et en déchiffrant un message.

    """
     # Générer les clés publiques

    public_key, private_key = generate_keys(bits)
    p, g, A = public_key
    _, a = private_key
    result = calcul_log_discret(g, A, p)
    # résultat dans la queue
    queue.put((result, a))


@pytest.mark.parametrize("bits", [16, 128])
def test_log_discret_resistance(bits):
    """
    Vérifie qu'il n'est pas possible (ou pas facile) de retrouver la clé privée a
    à partir de la clé publique (p, g, A) par attaque du logarithme discret à partir de 21 bits.
    """

    queue = Queue()
    proc = Process(target=attaque, args=(bits, queue))
    proc.start()
    proc.join(timeout=60)

    # Si le processus est toujours vivant après 30 secondes, on le termine
    if proc.is_alive():
        proc.terminate()
        proc.join()
        # Plus de 30 secondes → test réussi
        assert True
    else:
        result, a = queue.get()
        if bits <= 20:
            assert result == a, f"[ÉCHEC] Résultat incorrect pour {bits} bits"
        else:
            assert result != a, f"[ÉCHEC] Le log discret a réussi trop vite pour {bits} bits"