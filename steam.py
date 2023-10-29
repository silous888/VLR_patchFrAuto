import winreg
import os

import utils
import shutil


def trouver_dossier_steam():
    """recupère le chemin du dossier steam via les registres

    Returns:
        str: chemin du dossier steam
    """
    KEY_PATH_STEAM = r"SOFTWARE\\Valve\\Steam"
    KEY_NAME = "SteamPath"
    try:
        key_steam = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, KEY_PATH_STEAM, 0, winreg.KEY_READ
        )
        chemin_steam = winreg.QueryValueEx(key_steam, KEY_NAME)[0]
        return chemin_steam
    except:
        utils.logging.error("dossier steam non trouvé")


def extraire_path_dans_ligne(ligne):
    """récupère le path de la steamlibrary de la ligne du fichier libraryfolders.vdf
                "path"		"F:\\SteamLibrary"
    la ligne se présente comme ceci, on récupère le string situé entre les 3ème et 4ème guillemets

    Args:
        ligne (str): ligne de libraryfolders.vdf où est le situé le chemin de la steamlibrary

    Returns:
        int, int: début et fin de la sous-chaine de la ligne présentant le chemin de la steamlibrary
    """
    compteur_apostrophes = 0
    index_debut = 0
    index_fin = 0
    for index, caractere in enumerate(ligne):
        if caractere == '"':
            compteur_apostrophes += 1
            if compteur_apostrophes == 3:
                index_debut = index + 1
            if compteur_apostrophes == 4:
                index_fin = index
    return index_debut, index_fin


def trouver_dossiers_jeux(chemin_steam):
    """ouvre le fichier libraryfolders.vdf présent dans le dossier steam pour trouver les path des steamlibrary

    Args:
        chemin_steam (str): chemin absolu du répertoire steam

    Returns:
        list(str): liste des chemin des steamlibrary
    """
    dossiers_jeux = []
    fichier_libraryfolders = chemin_steam + "\\steamapps\\libraryfolders.vdf"
    if os.path.exists(fichier_libraryfolders):
        with open(fichier_libraryfolders, "r") as fichier:
            for ligne in fichier:
                if ligne.find("path") != -1:  # si on trouve "path" dans la ligne
                    index_debut, index_fin = extraire_path_dans_ligne(ligne)
                    path = utils.convertir_double_slash_en_simple(
                        ligne[index_debut:index_fin]
                    )
                    dossiers_jeux.append(path)
    else:
        utils.logging.error("fichier libraryfolders.vdf non trouvé")
    return dossiers_jeux


def trouver_bin_zero_escape(nom_bin):
    """récupère le chemin absolu du bin du dossier steam du jeu
    
    Args:
        nom_bin (str): nom du bin du jeu, sans le .bin
    Returns:
        str: chemin du ze1_data.bin
    """
    dossier_steam = trouver_dossier_steam()
    dossiers_jeux = trouver_dossiers_jeux(dossier_steam)
    for chemin in dossiers_jeux:
        chemin_complet = (
            chemin + "\\steamapps\\common\\Zero Escape The Nonary Games\\" + nom_bin + ".bin"
        )
        if os.path.exists(chemin_complet):
            return chemin_complet
    utils.logging.error("bin non trouvé")
    return -1


def copier_fichier_progression(src, dst, callback):
    """copie un fichier

    Args:
        src (str): chemin du fichier source
        dst (str): chemin du dossier de destination
        callback (function): fonction d'affichage de la progression
    """
    with open(src, "rb") as source_file, open(dst, "wb") as dest_file:
        taille_fichier = os.path.getsize(src)
        total_copie = 0
        morceau = (
            4096  # Taille du morceau pour copier
        )

        while True:
            morceau_data = source_file.read(morceau)
            if not morceau_data:
                break

            dest_file.write(morceau_data)
            total_copie += len(morceau_data)

            # Appel de la fonction pour afficher la progression
            callback(total_copie, taille_fichier)


def afficher_progression(copie, total):
    """affiche dans la console la progression de la copie du fichier

    Args:
        copie (int): taille actuelle de la copie
        total (int): taille totale du fichier
    """
    pourcentage = (copie / total) * 100
    print(f"Progression : {copie}/{total} octets copiés ({pourcentage:.2f}%)")


def copier_bin_dans_VLR_data_patch(chemin_bin):
    """copie le ze1_data.bin dans le dossier bin_org du programme

    Args:
        chemin_bin (str): chemin absolu du ze1_data.bin du dossier steam du jeu
    """
    dossier_tool = "VLR_patch_data\\org_bin"
    dossier_projet = utils.get_exe_directory()
    dossier_tool_complet = dossier_projet + "\\" + dossier_tool
    utils.logging.error(dossier_tool_complet)

    shutil.copy(chemin_bin, dossier_tool_complet)
