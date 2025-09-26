def chiffrement_vigenere(texte_clair : str, clef : str) -> str:
    # le chiffrement ne doit fonctionner que si la clef et le texte clair sont composés uniquement de lettres 
    # (majuscules, minuscules ou combinaisons des deux)
    #les espaces, signes de ponctuations et caractères spéciaux sont aussi pris en compte dans le texte clair mais ne sont pas chiffrés
    #la clef est répétée autant de fois que nécessaire pour chiffrer tout le texte clair
    #le chiffrement n'est pas sensible à la casse (on peut chiffrer avec une clef en majuscules, minuscules ou combinaison des deux)
    #le résultat doit être en majuscules
    texte_chiffre : str
    texte_chiffre = ""
    longueur_clef : int
    longueur_clef = len(clef)
    index_clef : int
    index_clef = 0
    index_texte : int
    index_texte = 0
    caractere_clef : str
    caractere : str

    for caractere in texte_clair :
        if caractere.isalpha():
            #Prend le caractère de la clef en fonction de l'index
            caractere_clef = clef[index_clef % longueur_clef].upper()
            # Convertit les deux caractères en majuscules et calcule leur position dans l'alphabet {0,25}
            c_val = ord(caractere.upper()) - ord('A')
            k_val = ord(caractere_clef) - ord('A')
            # Applique la formule de chiffrement de Vigenère
            chiff_val = (c_val + k_val) % 26
            texte_chiffre += chr(chiff_val + ord('A'))
            index_clef += 1
        else:
            # Si le caractère n'est pas une lettre, on l'ajoute tel quel au texte chiffré
            texte_chiffre += caractere
        index_texte += 1
    
    return texte_chiffre

                


if __name__ == "__main__" :
    texte_clair : str
    clef : str
    texte_chiffre : str
    texte_clair = input(str("Entrez le texte à chiffrer : "))
    clef = input(str("Entrez la clef de chiffrement : "))
    texte_chiffre = chiffrement_vigenere(texte_clair, clef)
    print("Le texte chiffré est : ", texte_chiffre)

    