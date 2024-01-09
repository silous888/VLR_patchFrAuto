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
