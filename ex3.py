"""
Usage (ligne de commande) :
  python kasiski_vigenere.py --kasiski <fichier_chiffre>
  python kasiski_vigenere.py --test      # lance les jeux d'essais inclus

Fonction disponible dans ce fichier :
 - kasiski_key_length(ciphertext, min_len=3, max_len=16)
 - 

Décisions de traitement (à justifier dans le rapport) :
 - Pour Kasiski on travaille sur une version filtrée du texte : on ne conserve que les lettres
   A-Za-z (on passe tout en majuscules) car les répétitions utiles pour Kasiski portent sur la
   séquence de lettres. Les espaces/ponctuation sont ignorés pour la recherche des répétitions.
 - On considère des fragments de longueur >= min_len (par défaut 3). On recherche toutes les
   répétitions pour les longueurs entre min_len et max_len (inclus), puis on les ordonne par
   longueur décroissante (fragment le plus long en premier) comme demandé.
 - Pour chaque fragment répété on calcule les distances entre positions successives des occurrences.
 - Les candidats initiaux pour la taille de la clé sont les diviseurs (>1) de la première distance
   rencontrée (première ligne du tableau repet).
 - On applique l'algorithme décrit (PGCD itératif entre candidats et distance), en éliminant 1.

Sortie de kasiski_key_length:
 - retourne une liste d'entiers possibles pour la longueur de la clé, ou une liste vide si aucune
   hypothèse n'a pu être formulée (équivalent au symbole '?').

"""

from collections import defaultdict
from math import gcd
import argparse
import sys
import itertools
import textwrap


def only_letters_upper(s: str) -> str:
    """Garde uniquement les lettres et convertit en majuscules."""
    return ''.join(ch.upper() for ch in s if ch.isalpha())


def divisors(n: int):
    """Retourne la liste des diviseurs de n strictement supérieurs à 1, triés croissants."""
    res = []
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            res.append(d)
            other = n // d
            if other != d:
                res.append(other)
    if n > 1:
        res.append(n)
    return sorted(set(res))


def find_repetitions(cipher_filtered: str, min_len=3, max_len=None):
    """
    Trouve les fragments répétés (taille >= min_len) dans cipher_filtered (chaîne de lettres, majuscules).
    Retourne une liste de tuples (fragment, [positions], length) triée par length desc.
    positions are start indices (0-based) in cipher_filtered.
    """
    n = len(cipher_filtered)
    if max_len is None:
        max_len = max(min_len, n // 2)
    max_len = min(max_len, n)

    found = []
    # On recherche longueurs descendantes pour faciliter l'ordonnancement demandé
    for L in range(max_len, min_len - 1, -1):
        table = defaultdict(list)
        for i in range(0, n - L + 1):
            frag = cipher_filtered[i:i+L]
            table[frag].append(i)
        for frag, poslist in table.items():
            if len(poslist) >= 2:
                found.append((frag, poslist, L))
    return found


def kasiski_key_length(ciphertext: str, min_len=3, max_len=16):
    """
    Applique la méthode de Kasiski sur ciphertext et retourne une liste de candidats pour
    la longueur de la clé (ou [] si aucune hypothèse).

    - ciphertext : texte chiffré (peut contenir ponctuation). On filtrera pour ne garder
      que les lettres (majuscule) pour la recherche de répétitions.
    - min_len : longueur minimale du fragment répété (par défaut 3)
    - max_len : longueur maximale des fragments à considérer (par défaut 16)
    """
    filtered = only_letters_upper(ciphertext)
    if len(filtered) < min_len * 2:
        return []

    repet = find_repetitions(filtered, min_len=min_len, max_len=max_len)
    if not repet:
        return []

    repet_table = []  # list of (frag, distance)
    for frag, poslist, L in repet:
        # calculer distances successives entre positions
        for i in range(1, len(poslist)):
            distance = poslist[i] - poslist[i-1]
            if distance > 0:
                repet_table.append((frag, distance, L, poslist[0], poslist[i]))

    # trier le tableau par taille du fragment (déjà ordre desc) puis par distance (optionnel)
    repet_table.sort(key=lambda x: (-x[2], x[1]))

    # Si vide -> échec
    if not repet_table:
        return []

    # Étape 5 : candidats = diviseurs(distance de la première ligne)
    first_distance = repet_table[0][1]
    candidats = divisors(first_distance)

    # si aucun diviseur (improbable avec >1), pas d'hypothèse
    if not candidats:
        return []

    # Étape 6 : parcourir le tableau ligne par ligne
    for (frag, distance, L, p1, p2) in repet_table[1:]:
        temp = []
        for c in candidats:
            g = gcd(c, distance)
            if g > 1:
                temp.append(g)
        temp = sorted(set(temp))
        if temp:
            candidats = temp
        else:
            # si temp vide : garder candidats tels quels et continuer 
            continue

    # À la fin, retourner candidats (éventuellement vides)
    return sorted(set(candidats))


def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=textwrap.dedent('''
                                 Kasiski pour Vigenere
                                 '''))
    ap.add_argument('--kasiski', help='fichier contenant le texte chiffré (utf-8)')
    ap.add_argument('--min', type=int, default=3, help='longueur min des fragments (defaut 3)')
    ap.add_argument('--max', type=int, default=16, help='longueur max des fragments (defaut 16)')
    args = ap.parse_args()

    

    if args.kasiski:
        try:
            with open(args.kasiski, 'r', encoding='utf-8') as f:
                txt = f.read()
        except Exception as e:
            print('Impossible de lire le fichier:', e, file=sys.stderr)
            sys.exit(2)
        candidates = kasiski_key_length(txt, min_len=args.min, max_len=args.max)
        if not candidates:
            print('Aucune hypothèse (retour: ? / liste vide)')
        else:
            print('Candidats pour la taille de la clé:', candidates)
        return

    ap.print_help()


if __name__ == '__main__':
    main()
