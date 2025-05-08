# Calcul biparti et transfert inconscient groupe 2

## Installer les bibliothèques nécessaires

Il suffit d'exécuter la commande suivante : `pip install -r requirments.txt`

## Tester le code

Il suffit d'exécuter la commande suivante : `python -m pytest test/`
C'est également possible de tester uniquement une partie du code, par exemple :
`python -m pytest test/garbled_circuit`

# Circuit Brouillé - BEN EL MOSTAPHA Mohamed

## Vue général

### Le fichier `ctr.py`

Dans le package `garbled_circuit`, j'ai implémenté le chiffrement en mode compteur en utilisant la bibliothèque `pycryptodome` pour accéder à la fonction AES classique.

### Le fichier `garbler.py`

Ce fichier implémente une variation du circuit brouillé dite _"Point and Permute"_. Contrairement à la version classqiue, qui utilise un MAC pour confirmer le bon fonctionnement du déchiffrement, cette version utilise les derniers bits des labels pour calculer la position exact à déchiffrer dans la table de vérité.

Exemple :

Label 1 : 101001....1 (en binaire)
Label 2 : 101000....0 (en binaire)

Position à déchiffrer : 10 (soit 2 en décimale)

## Détails de l'implémentation

### Mode compteur

`encrypt_ctr(key: int, message: int, nonce: int)` : Prend une clé de longueur 128 bits, un message de longueur quelconque et une valeur aléatoire. Le message
est divisé en blocs de 128 bits, éventuellement avec du bourage. La bloque i est masqué (mis en xor avec une valeur) par un masque généré à l'aide de la valeur `nonce + i`. Le masque n'est autre que le chiffrement de `nonce + i` par la fonction AES standard.

### Circuit Brouillé

`generate_wire_labels(circuit : CircuitCombinatoire)` : étant donné un circuit, produit une table qui associé à chaque noeud un tuple `(label0, label1)` ou les labels sont des valeurs aléatoire de longueur inférieure ou égale à 128 bits, sauf pour les noeud de sorties qui sont associé à `(0, 1)`.
`label0` : représente la valuer 0 pour le noeud concerné dans le circuit brouillé
`label1` : représente la valuer 1 pour le noeud concerné dans le circuit brouillé
Le dernier bit de `label0`, soit `label0 & 1`, est opposé à celui de `label1`. Cette propriété sera utilisé pour l'implémentation du `Point and Permute` décrite çi-dessus.

`get_index_from_input_labels(label_input_list)` : étant donnée une liste de labels, calcule la position généré en concatenant le dernier bit du label i à la position i du résultat.

`encrypt_output_label_with_input_labels(label_input_list, output_label, nonce)` : étant donnée une liste de labels, un label de sortie et une valeur aléatoire, chiffre le label de sortie `len(label_input_list)` fois, en utilisant le i-ème label comme clé et le résultat du dernier chiffrement comme message pour la fonction `encrypt_ctr`.

`decrypt_encrypted_output_label_with_input_labels(label_input_list, encrypted_output_label, nonce)` : applique le même algorithme que la fonction de chiffrement en inversant la liste de labels.

`binary_to_label_list(binary_list, label_tuples)` :
étant données une liste de valeurs binaire et une liste de tuples `(label0, label1)`, produit une liste où chaque 1 ou 0 à la position i est remplacé par label0 ou label1 respectivement.

`get_input_possibilities(node : Node)` : Selon l'étiquette du noeud, renvoie une liste d'entrées possibles.

`garble(circuit : CircuitCombinatoire, wire_labels, nonce)` : Pour chaque noeud du circuit :

1. Retrouve ses noeuds d'input
2. Initialise une table de hachage qui va associer à chaque noeud une table de vérité
3. Calcule les inputs possible selon le type du noeud, et pour chaque possibilité :
   3.1. Calcule l'output pour cette possiblité et le traduit en label
   3.2. traduit la liste d'input en labels
   3.3. Utilise cette liste de labels pour chiffrer le label d'output en utilisant `encrypt_output_label_with_input_labels`
   3.4. Met le résultat de ce chiffrement en la position calculé en utilisant `get_index_from_input_labels`
4. Renvoie la table de hachage qui associe à chaque noeud sa table de vérité

`evaluate(circuit : CircuitCombinatoire, garbled_circuit_tables, wire_values, nonce)` : `wire_values` est une table de hachage qui associe à chaque noeud sa valeur courante (son état). On s'attend à ce que les noeud d'input dans cette table soient initialise avec les labels souhaités. Pour chaque noeud, la fonction calcule la liste de label d'entré et l'utilise pour trouver la position à déchiffrer sur la table de tables de vérités.
