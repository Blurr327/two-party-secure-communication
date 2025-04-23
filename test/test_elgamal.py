import pytest
from elGamal import generate_keys, encrypt, decrypt

def test_elgamal(bits=10, msg=5):
    """
    Fonction pour tester l'algorithme ElGamal en générant les clés,
    en chiffrant et en déchiffrant un message.

    """
    # Générer les clés publiques et privées d'Alice
    public_key, private_key = generate_keys(bits)

    # Chiffrement du m par Bob
    crypted_m = encrypt(public_key, msg)
    print("m chiffré (B, c) = " ,crypted_m)

    # Déchiffrement du m par Alice
    decrypted_m = decrypt(private_key, crypted_m)
    print("m déchiffré = ", decrypted_m)
    
    # Vérification que le message déchiffré est le même que celui d'origine
    assert decrypted_m == msg, f"Erreur : message déchiffré {decrypted_m} n'est pas égal au message original {msg}"