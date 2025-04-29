from transfert_inconscient.elGamal import generate_keys,encrypt,decrypt
import random

rdm = random.SystemRandom()

  
def alice_prepare(p) :
    
    # les messages m0, m1 sont des éléments de G.
    
    m0 = rdm.randint(1, p-1)
    m1 = rdm.randint(1, p-1)
    
    # Elément aléatoire C dans G, on exclut 1 et p-1 pour éviter de casser le protocole, p-1 pourrait réveler une symétrie,...
    
    C = rdm.randint(2,p-2)
    
    return m0,m1,C
    
def alice_encrypt(p, g, A0, A1, m0, m1):
    
    #Alice chiffre m0 et m1 avec Elgamal en utilisant les cles publiques A0,A1 et envoie à Bob
    
    c0=encrypt((p, g, A0),m0)
    c1=encrypt((p, g, A1),m1)
    
    return c0, c1

def bob_prepare(p, g, C):
    
    # Bob choisit un bit b aléatoire, génère a, envoie (A0,A1)
    
    b = rdm.randint(0, 1)
        
    # On exclut p-1 car pour a= p-1 on a g^(p−1)=1 à cause du petit théorème de Fermat
    
    a = rdm.randint(1, p-2)
    Ab= pow(g,a,p)
    A1_b = (C*pow(Ab,-1,p)) % p
    
    if b==0:
        A0 = Ab
        A1 = A1_b 
    else:
        A0 = A1_b 
        A1 = Ab
    
    return b, a, A0, A1

def bob_decrypt(p,a,b,c0,c1):
    
    # Bob déchiffre le message pour lequel il dispose la clé publique a
    
    c = c0 if b == 0 else c1
    m_decoded = decrypt((p,a),c)
    
    return m_decoded


def ot_protocol(bits):
    
    # Etape 1 :
    
    # Alice sélectionne un groupe G d’ordre p premier avec générateur g
    
    # génération des clés
    public_key_a,private_key_a = generate_keys(bits)
    p,g,A = public_key_a
    
    # description de G (p,g)
    print(f"Alice choisit p={p}, g={g}")
    
    
    m0, m1, C = alice_prepare(p)
    
    print(f"Message d'Alice : m0 = {m0}, m1 = {m1}")
    
    print(f"Alice envoie C = {C} à Bob")
    
    # Etape 2 :
    
    b, a, A0, A1 = bob_prepare(p, g, C)
    
    print(f"Bob choisit le bit b = {b}")
        
    print(f"Bob envoie (A0,A1) = ({A0},{A1}) à Alice")
    
    # Etape 3 :
    
    #Alice vérifie que A0*A1 = C
    
    if (A0 * A1) % p != C:
        raise ValueError("La vérification d'A0*A1 = C (mod p) a échoué.")
    
    c0, c1 = alice_encrypt(p, g, A0, A1, m0, m1)
    
    print(f"Alice envoie les messages chiffrés (c0, c1) = ({c0}, {c1}) à Bob")
    
    # Etape 4 :
    
    m_decoded = bob_decrypt(p, a, b, c0, c1)
    
    print(f"Bob déchiffre et obtient m{b} = {m_decoded}")

    return m0, m1, b, m_decoded
    
