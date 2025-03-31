import secrets #module utilisé pour générer des grand nb random pour crypto
import random
rdm = random.SystemRandom()

# Test de primalité de Miller-Rabin
def single_test(n: int, a: int) -> bool:
    exp = n - 1
    while exp % 2 == 0:  # Tant que exp est pair
        exp //= 2
    if pow(a, exp, n) == 1:
        return True
    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True
        exp *= 2
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

def gen_prime(bits: int) -> int:
    while True:
        a = (rdm.randrange(1 << (bits - 1), 1 << bits) << 1) + 1  # Nombre impair
        if is_prime_miller_rabin(a):
            return a
        