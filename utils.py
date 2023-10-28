import logging
import os
import sys

# Configuration des logs
logging.basicConfig(
    level=logging.DEBUG,  # Niveau de journalisation (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format des messages de log
    filename="app.log",  # Nom du fichier de log
    filemode="w",  # Mode d'écriture du fichier ('w' pour écrire à chaque fois)
)


def convertir_double_slash_en_simple(path):
    """converti les slash \ en double slash dans un chaine de caractère, pour éviter les problèmes

    Args:
        path (str): path windows

    Returns:
        str: path windows avec des double slash à la place des simples
    """
    return path.replace("\\\\", "\\")


def remplace_apostrophe(texte):
    """remplace les apostrophes par le caractère Ｓ

    Args:
        texte (str): texte à modifier

    Returns:
        str: texte modifié
    """
    return texte.replace("'", "Ｓ")


def remplace_guillemet(texte):
    """remplace les guillemets par le caractère Ｄ

    Args:
        texte (str): texte à modifier

    Returns:
        str: texte modifié
    """
    return texte.replace('"', "Ｄ")


def supprime_amp(texte):
    """suprime les "amp;" d'un texte, c'est le code du caractère &

    Args:
        texte (str): texte à modifier

    Returns:
        str: texte modifié
    """
    return texte.replace("amp;", "")


def get_valeur_progression(actuelle, total):
    """renvoie le pourcentage de la progression actuelle

    Args:
        actuelle (int): progression actuelle
        total (int): valeur max de la progression

    Returns:
        int: entier du pourcentage de la progression
    """
    return round(actuelle / total * 100)


def get_exe_directory():
    """renvoie le chemin absolu du chemin où est situé le dossier de l'exécutable, ou le .py exécuté

    Returns:
        str: chemin absolu du dossier de l'exécutable
    """
    exe_path = os.path.abspath(sys.argv[0])
    exe_dir = os.path.dirname(exe_path)
    return exe_dir



def concat_listes(liste1, liste2):
    return [elem1 + " - " + elem2 for elem1, elem2 in zip(liste1, liste2)]


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