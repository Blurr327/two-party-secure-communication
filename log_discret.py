import math

def calcul_log_discret(g: int, y: int, p: int) -> int | None:

# Étape 1 : Initialisation
    t: int = math.isqrt(p)  # t = ⌊√p⌋

# Étape 2 : Création du dictionnaire (grands pas)
    grands_pas: dict[int,int] = []
    for i in range(t+1) :
        grands_pas[pow(g,i*t,p)] = i
    #on trie par rapport à la 1ere composante du tuple, donc de la puissance calculée
    grands_pas_list = list(grands_pas.items()) # je fais ça pour pouvoir trier car on ne peut pas trier un dictionnaire
    grands_pas_list.sort(key=lambda t : t[0]) # nlogn

# Étape 3 : Recherche des collisions (grands pas)

    for i in range(t+1):
        valeur: int = (y * pow(g, i, p)) % p
        # en théta 1 (askip)
        if valeur in grands_pas :
        # Étape 4 : Calcul de x à partir des indices i et k
            k: int = grands_pas[valeur]
            return (k * t + i)%(p-1)

    # Si aucune solution n'est trouvée
    return None

# Exemple d'utilisation
g: int = 2      # générateur de (Z/29Z)*
y: int = 22     # l'élément dont on cherche le log en base g 
p: int = 29     # Nombre premier (modulo)

resultat: int | None = calcul_log_discret(g, y, p)
if resultat is not None:
    print(f"La solution est x = {resultat}")
else:
    print("Aucune solution trouvée.")
