def etats_true(liste_de_listes):
    for sous_liste in liste_de_listes:
        for element in sous_liste:
            if not element:
                return False
    return True


def etats_false(liste_de_listes):
    for sous_liste in liste_de_listes:
        for element in sous_liste:
            if element:
                return False
    return True


def etats_liste(liste_de_listes):
    if etats_true(liste_de_listes):
        return 1
    if etats_false(liste_de_listes):
        return -1
    return 0


def remplace_guillemet(texte):
    """remplace les guillemets par le caractère Ｄ

    Args:
        texte (str): texte à modifier

    Returns:
        str: texte modifié
    """
    return texte.replace('"', "\\\"")


def get_valeur_progression(actuelle, total):
    """renvoie le pourcentage de la progression actuelle

    Args:
        actuelle (int): progression actuelle
        total (int): valeur max de la progression

    Returns:
        int: entier du pourcentage de la progression
    """
    return round(actuelle / total * 100)
