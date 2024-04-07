import API.steam_game_api as steamGameAPI

import filelist
import gestionLUA
import googleSheetAPI
import matSheet
import utils
import ze2_tool


import os
import shutil
import time


TOTAL_PROGRESS = (
    len(filelist.LIST_FILENAME_ARCHIVE_ENG)
    + len(filelist.LIST_FILENAME_SYSTEM_ENG)
    + len(filelist.LIST_FILENAME_ESCAPE_ENG)
    + len(filelist.LIST_FILENAME_NOVEL_ENG)
    + 20
)
current_progress = 0


def get_bin_vlr():
    if not os.path.exists(".\\VLR_patch_data\\org_bin\\ze2_data_jp.bin"):
        steamGameAPI.copy_data_from_steam_game_folder("Zero Escape The Nonary Games",
                                                      ".\\VLR_patch_data\\org_bin\\",
                                                      data_to_copy="ze2_data_jp.bin",
                                                      overwrite=False)


def copy_fnt_fr_in_patch_res():
    source = "VLR_patch_data\\fnt_fr\\"
    destination = "VLR_patch_data\\patch_res\\"

    for file in os.listdir(source):
        path_source = os.path.join(source, file)
        path_destination = os.path.join(destination, file)

        shutil.copy2(path_source, path_destination)


def compile_game(path_bin_steam):
    path_bin_software = "VLR_patch_data\\patch_bin\\ze2_data_jp.bin"
    ze2_tool.patch_files()
    copy_fnt_fr_in_patch_res()
    ze2_tool.repack_ze2_bin()
    time.sleep(0.3)
    shutil.move(path_bin_software, path_bin_steam)
    steamGameAPI.copy_data_in_steam_game_folder("Zero Escape The Nonary Games", path_bin_software)


def gestion_NOVEL(instance_worker):
    """modifie les fichiers NOVEL

    Args:
        instance_worker (worker): sert pour update la progression
    """
    liste_choix_fichiers_NOVEL = instance_worker.liste_choix_fichiers[1]
    for index, file in enumerate(filelist.LIST_FILENAME_NOVEL_ENG):
        if liste_choix_fichiers_NOVEL[index]:
            update_text_progression(instance_worker, file)
            modif_lua_file(instance_worker, index, matSheet.NomsColonnes.DIALOGUE)
            incrementer_progression(instance_worker)


def modif_lua_file(instance_worker, file_index, nomColonne):
    instance_worker.set_text_progress(filelist.LIST_FILENAME_NOVEL_ENG[file_index])
    mat = recup_mat_sheet_simplifie(filelist.LIST_FILENAME_NOVEL_ENG[file_index], nomColonne)
    if nomColonne == matSheet.NomsColonnes.DIALOGUE:
        gestionLUA.modifier_texte_dans_fichier(filelist.LIST_FILENAME_NOVEL_JP[file_index], mat)
    else:
        gestionLUA.modifier_texte_dans_fichier_system(filelist.LIST_FILENAME_SYSTEM_JP[file_index], mat)


def recup_mat_sheet_simplifie(fichier, noms_colonnes):
    """_summary_

    Args:
        fichier (str): fichier xml à traiter
        noms_colonnes (list\[3](str)): noms des colonnes pour ce fichier
        double_id (bool, optional): True si fichier avec double id. Defaults to False.

    Returns:
        elementTree, list(element), list(list\[3](str)): arbre, liste des éléments avec texte
        et matrice des données importante du sheet
    """
    mat_sheet = googleSheetAPI.get_matrice_sheet(fichier)
    mat_sheet_simp = matSheet.get_matrice_simplifie(mat_sheet, noms_colonnes)
    return mat_sheet_simp


def incrementer_progression(instance_worker, value=1):
    global current_progress
    current_progress = current_progress + value
    instance_worker.set_value_progressbar(
        utils.get_valeur_progression(current_progress, TOTAL_PROGRESS)
    )


def update_text_progression(instance_worker, message):
    instance_worker.set_text_progress(message)
