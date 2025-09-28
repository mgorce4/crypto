# Alphabet étendu : lettres (majuscules/minuscules), accents, chiffres, ponctuation
ALPHABET = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "ÀÂÄÇÉÈÊËÎÏÔÖÙÛÜàâäçéèêëîïôöùûü"
    "0123456789"
    " .,;:!?()[]{}+-*/=<>_\"'&%$#@^~|\\"
)

def get_k_val(caractere_clef: str) -> int:
    """Décalage de la clé en fonction de l'alphabet étendu"""
    if caractere_clef in ALPHABET:
        return ALPHABET.index(caractere_clef)
    else:
        # Si le caractère n’est pas dans l’alphabet → on prend son code Unicode mod taille alphabet
        #pour éviter les erreurs
        return ord(caractere_clef) % len(ALPHABET)


def chiffrement_vigenere_complet(texte_clair: str, clef: str) -> str:
    texte_chiffre = ""
    longueur_clef = len(clef)
    index_clef = 0
    n = len(ALPHABET)

    for caractere in texte_clair:
        k_val = get_k_val(clef[index_clef % longueur_clef])

        if caractere in ALPHABET:
            c_val = ALPHABET.index(caractere)
            chiff_val = (c_val + k_val) % n
            texte_chiffre += ALPHABET[chiff_val]
        else:
            # Si caractère inconnu → inchangé
            texte_chiffre += caractere

        index_clef += 1

    return texte_chiffre


def dechiffrement_vigenere_complet(texte_chiffre: str, clef: str) -> str:
    texte_clair = ""
    longueur_clef = len(clef)
    index_clef = 0
    n = len(ALPHABET)

    for caractere in texte_chiffre:
        k_val = get_k_val(clef[index_clef % longueur_clef])

        if caractere in ALPHABET:
            c_val = ALPHABET.index(caractere)
            dechiff_val = (c_val - k_val + n) % n
            texte_clair += ALPHABET[dechiff_val]
        else:
            texte_clair += caractere

        index_clef += 1

    return texte_clair

def chiffrement_de_vigenere_simple_en_majuscules(texte_clair: str, clef: str) -> str:
    texte_chiffre = ""
    longueur_clef = len(clef)
    index_clef = 0
    n = 26  # Nombre de lettres dans l'alphabet français (A-Z)

    for caractere in texte_clair:
        if caractere.isalpha():  # Vérifie si le caractère est une lettre
            k_val = ord(clef[index_clef % longueur_clef].upper()) - ord('A')
            c_val = ord(caractere.upper()) - ord('A')
            chiff_val = (c_val + k_val) % n
            texte_chiffre += chr(chiff_val + ord('A'))
            index_clef += 1
        else:
            texte_chiffre += caractere  

    return texte_chiffre

def dechiffrement_vigenere_simple_en_majuscules(texte_chiffre: str, clef: str) -> str:
    texte_clair = ""
    longueur_clef = len(clef)
    index_clef = 0
    n = 26  # Nombre de lettres dans l'alphabet français (A-Z)

    for caractere in texte_chiffre:
        if caractere.isalpha():  # Vérifie si le caractère est une lettre
            k_val = ord(clef[index_clef % longueur_clef].upper()) - ord('A')
            c_val = ord(caractere.upper()) - ord('A')
            dechiff_val = (c_val - k_val + n) % n
            texte_clair += chr(dechiff_val + ord('A'))
            index_clef += 1
        else:
            texte_clair += caractere  

    return texte_clair

if __name__ == "__main__":
    texte_clair : str
    clef : str
    texte_chiffre : str
    texte_dechiffre : str

    texte_clair = input("Entrez le texte à chiffrer : ")
    clef = input("Entrez la clef de chiffrement : ")
    texte_chiffre = chiffrement_de_vigenere_simple_en_majuscules(texte_clair, clef)
    print("Le texte chiffré est : ", texte_chiffre)
    texte_dechiffre = dechiffrement_vigenere_simple_en_majuscules(texte_chiffre, clef)
    print("Le texte déchiffré est : ", texte_dechiffre)
