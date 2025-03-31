import secrets #module utilisé pour générer des grand nb random pour crypto
import random
import math
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

#Fonction qui permet de générer un grand nombre premier
def gen_prime(bits: int) -> int:
    while True:
        a = (rdm.randrange(1 << (bits - 1), 1 << bits) << 1) + 1  # Nombre impair
        if is_prime_miller_rabin(a):
            return a
        
#Trouver un generateur de Zp* on veut que que g le generateur ait un ordre egal à p-1

#Pollard Rho algorithm
def prime_factors(n :int)->int:

    # no prime divisor for 1 
    if (n == 1):
        return n

    # even number : one of the divisors is 2 
    if (n % 2 == 0):
        return 2

    # we will pick from the range [2, N) 
    x = (random.randint(0, 2) % (n - 2))
    y = x

    # the constant in f(x).
    # Algorithm can be re-run with a different c
    # if it throws failure for a composite. 
    c = (random.randint(0, 1) % (n - 1))

    # Initialize candidate divisor (or result) 
    d = 1

    # until the prime factor isn't obtained.
    # If n is prime, return n 
    while (d == 1):
    
        # Tortoise Move: x(i+1) = f(x(i)) 
        x = (pow(x, 2, n) + c + n)%n

        # Hare Move: y(i+1) = f(f(y(i))) 
        y = (pow(y, 2, n) + c + n)%n
        y = (pow(y, 2, n) + c + n)%n

        # check gcd of |x-y| and n 
        d = math.gcd(abs(x - y), n)

        # retry if the algorithm fails to find prime factor
        # with chosen x and c 
        if (d == n):
            return prime_factors(n)
    
    return d

print(prime_factors(gen_prime(10)))


"""
def find_generator(p: int) -> int:
    if not is_prime_miller_rabin(p):
        raise ValueError("p doit être un nombre premier")
    
    q=p-1"""