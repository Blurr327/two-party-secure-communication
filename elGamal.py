import random
import math

rdm = random.SystemRandom()

# Test de primalité de Miller-Rabin
def single_test(n: int, a: int) -> bool:
    # Étape 1 : écrire n - 1 = 2^k * m avec m impair
    m = n - 1
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1

    # Étape 2 : calculer a^m mod n
    x = pow(a, m, n)
    if x == 1 or x == n - 1:
        return True

    # Étape 3 : vérifier a^{2^r * m} ≡ -1 mod n pour r = 0 .. k-1
    for _ in range(k - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True

    return False

def is_prime_miller_rabin(n: int, k=40) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for _ in range(k):
        a = rdm.randrange(2, n - 1)
        if not single_test(n, a):
            return False
    return True


#Fonction qui permet de générer un grand nombre premier
def gen_prime(bits: int) -> int:
    while True:
        a = rdm.randrange(1 << (bits - 1), 1 << bits)
        if a % 2 == 0:
            a+=1
        if is_prime_miller_rabin(a):
            return a
        
        
#Trouver un generateur de Zp* on veut que que g le generateur ait un ordre egal à p-1

#Pollard Rho algorithm (trouver des facteurs non triviaux): 
def pollard_rho(n: int) -> int :
    # Si le nombre est pair, on retourne 2 (trivial)
    if n % 2 == 0:
        return 2

    # Initialisation : choisir une valeur de départ aléatoire pour x dans [2, n-2]
    x = random.randint(2, n - 2)
    y = x  # y commence au même point que x
    c = random.randint(1, 10)  # Constante aléatoire pour la fonction f(x) = x^2 + c mod n
    d = 1  # Valeur initiale du diviseur

    # on continue tant qu'on n'a pas trouvé un diviseur non trivial
    while d == 1:
        # Mouvement "tortue" : une seule itération de f(x)
        x = (pow(x, 2, n) + c) % n

        # Mouvement "lièvre" : deux itérations de f(x)
        y = (pow(y, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        d = math.gcd(abs(x - y), n)

        # Si le diviseur est égal à n, l'algo a échoué → on recommence depuis le début
        if d == n:
            return pollard_rho(n) 

    return d

    
def remove_duplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

    
def prime_factors(n :int)-> list[int]:
    ret=[]
    
    if (n == 1):
        return ret

    while n % 2 == 0:
        ret.append(2)
        n //= 2

    if is_prime_miller_rabin(n):
        ret.append(n)
        return ret

    while n > 1:
        if is_prime_miller_rabin(n):
            ret.append(n)
            break
        
        factor = pollard_rho(n)
        while n % factor == 0:
            ret.append(factor)
            n//=factor
    return remove_duplicates(sorted(ret))


def puissances_n_mod_p(n: int, p: int) -> list[int]:
    l = [pow(n, i, p) for i in range(1,p)]
    return remove_duplicates(l)


"""
On sait que la taille de la liste doit faire p-1 pour generer Zp*

def is_gen(n: int, p: int) -> bool:
    if len(remove_duplicates(puissances_n_mod_p(n,p))) == p-1:
        return True
    return False
"""

def n_is_gen_Zp(n: int, p: int) -> bool:
    
    if not is_prime_miller_rabin(p):
        return False
    
    for q in prime_factors(p - 1):
        if pow(n, (p - 1) // q, p) == 1:
            return False
    return True


def generators_Zp_star(p: int) -> list[int]:
    return [g for g in range(2, p) if n_is_gen_Zp(g, p)]

def generate_keys(bits : int):
    
    p= gen_prime(bits)
    g= generators_Zp_star(p)[0]
    a= rdm.randrange(1, p-1)
    
    A = pow(g, a, p)
    
    public_key= (p, g, A)
    private_key= (p, a)
    
    return public_key, private_key

def encrypt(public_key, m : int):
    #on décompose public_key 
    p, g, A = public_key
    
    b = rdm.randrange(1, p-1)
    
    B = pow(g, b, p)
   
    c = (pow(A, b, p) * m) % p
    
    DH_key = (B,c)
    
    return DH_key

def decrypt(private_key, DH_key)->int:
    p, a = private_key
    B, c = DH_key
    
    x = p - 1 - a
    m = (pow(B , x , p)*c)%p
    
    return m
    
    
def test_elgamal(bits: int, msg: int):
    """
    Fonction pour tester l'algorithme ElGamal en générant les clés,
    en chiffrant et en déchiffrant un message.

    """
    # Générer les clés publiques et privées d'Alice
    public_key, private_key = generate_keys(bits)

    # Chiffrement du m par Bob
    crypted_m = encrypt(public_key, msg)
    print("m chiffré (B, c) = " + str(crypted_m))

    # Déchiffrement du m par Alice
    decrypted_m = decrypt(private_key, crypted_m)
    print("m déchiffré = "+ str(decrypted_m))
    
test_elgamal(10,5)