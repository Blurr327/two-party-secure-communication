import math
from typing import List, Tuple, Optional

def recherche_dichotomique(
    liste: List[Tuple[int, int]],
    valeur_cible: int,
    debut: int = 0,
    fin: Optional[int] = None
) -> Tuple[int, int] | None :
    
    if fin is None:
        fin = len(liste) - 1

    if debut > fin:
        return None
    
    milieu = (debut + fin) // 2
    couple = liste[milieu]
    valeur_actuelle = couple[1]  # On compare avec la 2ème composante
    
    if valeur_actuelle == valeur_cible:
        return couple
    elif valeur_actuelle < valeur_cible:
        return recherche_dichotomique(liste, valeur_cible, milieu + 1, fin)
    else:
        return recherche_dichotomique(liste, valeur_cible, debut, milieu - 1)

def calcul_log_discret(g: int, y: int, p: int) -> int | None:

# Étape 1 : Initialisation
    t: int = math.isqrt(p)  # t = ⌊√p⌋

# Étape 2 : Création de la liste chaînée (grands pas)
    grands_pas: list[tuple[int,int]] = []
    for i in range(t+1) :
        grands_pas.append((i,(g**(i*t))%p))

    #on trie par rapport à la 2e composante du tuple, donc de la puissance calculée
    grands_pas.sort(key=lambda t : t[1]) # nlogn

# Étape 3 : Recherche des collisions (grands pas)

    for i in range(t+1):
        valeur: int = (y * ((g**(i*t))%p)) % p
        # en théta 1 (askip)
        resultat_recherche : tuple[int,int] = recherche_dichotomique(grands_pas,valeur,0,None)
        if resultat_recherche != None and valeur == resultat_recherche[1] :
        # Étape 4 : Calcul de x à partir des indices i et k
            k: int = resultat_recherche[0]
            return (k * t - i)%(p-1)

    # Si aucune solution n'est trouvée
    return None

# Exemple d'utilisation
g: int = 2      # générateur de (Z/29Z)*
y: int = 22     # l'élément dont on cherche le log en base g 
p: int = 29     # Nombre premier (modulo)

resultat: int | None = calcul_log_discret(g, y, p)
if resultat is not None:
    print(f"La solution est x = {resultat}") # c'est censé être 26
else:
    print("Aucune solution trouvée.")
liste = [(1,1),(9,2),(4,3),(6,7),(1,9)]
resultat2 = recherche_dichotomique(liste,2,0,None)
print(resultat2)
