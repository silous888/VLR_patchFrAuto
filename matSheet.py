class NomsColonnes:
    """noms des 3 colonnes avec les données intéressantes pour chaque type de fichier
    la première colonne est celle de l'ID, ensuite celle du texte anglais, puis celle du texte français
    """

    DIALOGUE = ["id", "name", "text", "textFr"]
    SYSTEM = ["id", "id", "text", "textFr"]
    ARCHIVE = ["id", "text", "id_JP", "textJp", "id_FR", "textFr"]


def get_matrice_simplifie(mat, liste_noms_colonnes):
    """renvoie la matrice simplifié du sheet, avec seulement les données nécessaires

    Args:
        mat (list(list(str))): toutes les valeurs présentes dans la sheet
        liste_noms_colonnes (list[3](str)): les noms des colonnes dont on veut les valeurs

    Returns:
        list(list[4](str)): matrice avec les données intéressantes
    """
    try:
        position_id, position_name, position_eng, position_fr = get_positions_colonnes(mat[0], liste_noms_colonnes)
    except:
        print("valeur non trouvée")
        return []
    new_mat = []
    for i in range(1, len(mat)):  # les sheet ont des datas intéressantes à partir de la ligne 2
        if len(mat[i]) < 2:
            continue
        new_mat.append([mat[i][position_id], mat[i][position_name], mat[i][position_eng]])
        new_mat[-1].append(_ajouter_texte_fr_dans_mat_simp(mat[i], position_fr, position_eng))
    return new_mat


def _ajouter_texte_fr_dans_mat_simp(mat_ligne, position_fr, position_eng):
    """renvoie le texte à placer dans la colonne 3 de la ligne

    Args:
        mat_ligne (list(str)): ligne avec les valeurs à ajouter
        position_fr (int): position du texte fr dans la ligne
        position_eng (int): position du texte eng dans la ligne

    Returns:
        _type_: _description_
    """
    if len(mat_ligne) > position_fr and len(mat_ligne[position_fr]) > 0:
        return mat_ligne[position_fr]  # renvoie le texte fr s'il y en a un
    else:
        return mat_ligne[position_eng]  # sinon renvoie le texte anglais


def get_positions_colonnes(mat_ligne0, liste_noms_colonnes):
    """renvoie l'index des colonnes id eng et fr

    Args:
        mat_ligne0 (list): ligne 0 de la liste de liste du sheet
        liste_noms_colonnes (list[3](str)): nom des colonnes dont on veut l'index

    Returns:
        int, int, int: index de id, puis eng, puis fr
    """
    position_id = mat_ligne0.index(liste_noms_colonnes[0])
    position_name = mat_ligne0.index(liste_noms_colonnes[1])
    position_eng = mat_ligne0.index(liste_noms_colonnes[2])
    position_fr = mat_ligne0.index(liste_noms_colonnes[3])
    return position_id, position_name, position_eng, position_fr
