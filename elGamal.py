import secrets #module utilisé pour générer des grand nb random pour crypto
import random

#Génération clé Alice

#Test de primalité Fermat(pas très sécurisé)
def is_prime_test_fermat(n : int, k=5) -> bool:
    if n < 2:
        return False
    for _ in range(k):  # On fait k tests
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True

"""Test de primalité Miller Rabin"""
def single_test( n : int, a : int) -> bool:
    exp = n - 1
    while not exp & 1: #while paire(pas positif bit de fin)
        exp >> 1 # on coupe la fin
    if pow(a, exp, n) == 1: # un des termes est divisible par n
        return True
    while exp < n-1 :
        if pow(a,exp,n)==n-1:
            print("A faire !")

def is_prime_miller_rabin(n : int, k=5) -> bool:
    
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 ==0:
        return False
    
        
        
def generate_prime()-> int :
    print("")