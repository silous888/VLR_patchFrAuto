import zeVLRtool
import steam
import googleSheetAPI
import matSheet
import gestionLUA
import listeFichier
import utils
import os
import shutil
import time
from API import google_drive_api


TOTAL_PROGRESSION = (
    len(listeFichier.LISTE_NOM_FICHIER_SYSTEM)
    + len(listeFichier.LISTE_NOM_FICHIER_ARCHIVE)
    + len(listeFichier.LISTE_NOM_FICHIER_ESCAPE)
    + len(listeFichier.LISTE_NOM_FICHIER_NOVEL)
    + 20
)
progression_actuelle = 0


def recup_bin_ze_et_chemin_steam():
    """récupère le chemin du ze2_data_en_us.bin et le copie
    dans le dosssier bin_org s'il n'y est pas déjà, puis rename en ze2_data_jp

    Returns:
        str: chemin du ze1_data.bin du dossier steam du jeu
    """
    chemin_fichier = steam.trouver_bin_zero_escape("ze2_data_en_us")
    # utils.logging.error(chemin_fichier)
    if not os.path.exists("VLR_patch_data\\org_bin\\ze2_data_jp.bin") and not os.path.exists("VLR_patch_data\\org_bin\\ze2_data_en_us.bin"):
        steam.copier_bin_dans_VLR_data_patch(chemin_fichier)
    if not os.path.exists("VLR_patch_data\\org_bin\\ze2_data_jp.bin") and os.path.exists("VLR_patch_data\\org_bin\\ze2_data_en_us.bin"):
        os.rename("VLR_patch_data\\org_bin\\ze2_data_en_us.bin", "VLR_patch_data\\org_bin\\ze2_data_jp.bin")
    return chemin_fichier


def copy_fnt_fr_in_patch_res():
    source = "VLR_patch_data\\fnt_fr\\"
    destination = "VLR_patch_data\\patch_res\\"

    for fichier in os.listdir(source):
        chemin_source = os.path.join(source, fichier)
        chemin_destination = os.path.join(destination, fichier)

        shutil.copy2(chemin_source, chemin_destination)


def recompiler_jeu(chemin_bin_steam):
    """recompile le jeu avec les nouvelles data

    Args:
        chemin_bin_steam (str): chemin du ze1_data.bin du dossier steam du jeu
    """
    chemin_bin_us_logiciel = "VLR_patch_data\\patch_bin\\ze2_data_en_us.bin"
    if os.path.exists(chemin_bin_us_logiciel):
        os.remove(chemin_bin_us_logiciel)
    zeVLRtool.patch_fichiers()
    copy_fnt_fr_in_patch_res()
    zeVLRtool.repack_ze2_bin()
    time.sleep(0.3)
    os.rename("VLR_patch_data\\patch_bin\\ze2_data_jp.bin", chemin_bin_us_logiciel)
    shutil.move(chemin_bin_us_logiciel, chemin_bin_steam)


def gestion_NOVEL(instance_worker):
    """modifie les fichiers NOVEL

    Args:
        instance_worker (worker): sert pour update la progression
    """
    liste_choix_fichiers_NOVEL = instance_worker.liste_choix_fichiers[1]
    for index, fichier in enumerate(listeFichier.LISTE_NOM_FICHIER_NOVEL):
        if liste_choix_fichiers_NOVEL[index]:
            update_texte_progression(instance_worker, fichier)
            modif_fichier_lua(instance_worker, fichier, matSheet.NomsColonnes.DIALOGUE)
            incrementer_progression(instance_worker)


def gestion_ESCAPE(instance_worker):
    """modifie les fichiers ESCAPE

    Args:
        instance_worker (worker): sert pour update la progression
    """
    liste_choix_fichiers_ESCAPE = instance_worker.liste_choix_fichiers[0]
    for index, fichier in enumerate(listeFichier.LISTE_NOM_FICHIER_ESCAPE):
        if liste_choix_fichiers_ESCAPE[index]:
            update_texte_progression(instance_worker, fichier)
            modif_fichier_lua(instance_worker, fichier, matSheet.NomsColonnes.DIALOGUE)
            incrementer_progression(instance_worker)


def gestion_SYSTEM(instance_worker):
    """modifie les fichiers ESCAPE

    Args:
        instance_worker (worker): sert pour update la progression
    """
    liste_choix_fichiers_SYSTEM = instance_worker.liste_choix_fichiers[2]
    for index, fichier in enumerate(listeFichier.LISTE_NOM_FICHIER_SYSTEM):
        if liste_choix_fichiers_SYSTEM[index]:
            update_texte_progression(instance_worker, fichier)
            modif_fichier_lua(instance_worker, fichier, matSheet.NomsColonnes.SYSTEM)
            incrementer_progression(instance_worker)


def gestion_ARCHIVE(instance_worker):
    liste_choix_fichiers_ARCHIVE = instance_worker.liste_choix_fichiers[3]
    for index, fichier in enumerate(listeFichier.LISTE_NOM_FICHIER_ARCHIVE):
        if liste_choix_fichiers_ARCHIVE[index]:
            update_texte_progression(instance_worker, fichier)
            mat = googleSheetAPI.get_matrice_sheet_archive(fichier)
            gestionLUA.modifier_textes_dans_fichier_archive(fichier, mat)
            incrementer_progression(instance_worker)


def modif_fichier_lua(instance_worker, fichier, nomColonne):
    """modifier un fichier lua avec les valeurs récupérées dans le sheet
    associé, et enregistre le fichier

    Args:
        instance_worker (worker): sert pour update la progression
        fichier (str): fichier à modifier
        nomColonne (list[3](str)): noms des colonnes pour ce fichier
        double_id (bool, optional): True si fichier avec double id. Defaults to False.
    """
    instance_worker.set_text_progress(fichier)
    mat = recup_mat_sheet_simplifie(fichier, nomColonne)
    if nomColonne == matSheet.NomsColonnes.DIALOGUE:
        gestionLUA.modifier_texte_dans_fichier(fichier, mat)
    elif nomColonne == matSheet.NomsColonnes.SYSTEM:
        gestionLUA.modifier_texte_dans_fichier_system(fichier, mat)
    else:
        gestionLUA.modifier_textes_dans_fichier_archive(fichier, mat)


def recup_mat_sheet_simplifie(fichier, noms_colonnes):
    """_summary_

    Args:
        fichier (str): fichier xml à traiter
        noms_colonnes (list[3](str)): noms des colonnes pour ce fichier
        double_id (bool, optional): True si fichier avec double id. Defaults to False.

    Returns:
        elementTree, list(element), list(list[3](str)): arbre, liste des éléments avec texte
        et matrice des données importante du sheet
    """
    mat_sheet = googleSheetAPI.get_matrice_sheet(fichier)
    mat_sheet_simp = matSheet.get_matrice_simplifie(mat_sheet, noms_colonnes)
    return mat_sheet_simp


def incrementer_progression(instance_worker, valeur=1):
    """incrémente la barre de progression

    Args:
        instance_worker (worker): sert à accéder à la barre de progression
        valeur (int, optional): de combien on incrémente. Defaults to 1.
    """
    global progression_actuelle
    progression_actuelle = progression_actuelle + valeur
    instance_worker.set_value_progressbar(
        utils.get_valeur_progression(progression_actuelle, TOTAL_PROGRESSION)
    )


def update_texte_progression(instance_worker, message):
    """change le texte de progression

    Args:
        instance_worker (worker): sert à accéder à au label du texte
        message (str): texte à afficher
    """
    instance_worker.set_text_progress(message)


def gestion_images_DDS(instance_worker):
    if instance_worker.liste_choix_imagesdds[0][0]:
        id_dds_drive_folder = "1Fq52zamUcK-8tpUycsx8w8o-j--xQURX"
        path_dest = "VLR_patch_data\\patch_res\\"
        update_texte_progression(instance_worker, "téléchargement DDS")
        _ = google_drive_api.download_files_in_folder(id_dds_drive_folder, path_dest)
