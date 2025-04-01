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
def pollard_rho(n: int) -> int :
    #Cas n paire
    if n % 2 == 0:
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
            return pollard_rho(n)
    
    return d
    
#On sait que la taille de la liste doit faire p-1 pour generer Zp*
def remove_duplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

    
def prime_factors(n :int)-> list[int]:
    ret=[]
    # no prime divisor for 1 
    if (n == 1):
        return ret

    # even number : one of the divisors is 2 
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


a=gen_prime(10)-1
print(a)
print(prime_factors(a))


def gen(n: int, p: int) -> list[int]:
    return [pow(n, i, p) for i in range(1,p)]

#slide 139 à voir 

def is_gen(n: int, p: int) -> bool:
    if len(remove_duplicates(gen(n,p))) == p-1:
        return True
    return False

def generators(p : int ) -> list[int]:
    ret=[]
    factors=prime_factors(p-1)
    
    for i in range(len(factors)):
        if is_gen(factors[i],p):
            ret.append(factors[i])
    return ret

print(generators(13))
print(gen(2,13))
print(is_gen(2,13))
    

""" 
print(gen(2,13))
print(is_gen(2,13))
print(is_gen(2,12))

p=gen_prime(10)
g=prime_factors(p-1)
print(gen(g,p))
print(is_gen(g,p))
"""

    

def prime_fact(n : int):
    if is_prime_miller_rabin(n):
        return n
    

# Slide 145 cours trouver generateur dans Zp*
def find_generator(p: int) -> int:
    if not is_prime_miller_rabin(p):
        raise ValueError("p doit être un nombre premier")
    
    q=p-1