import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from credentials import credentials_info

class DossierDrive:
    """identifiant des différents dossier drive des sheets
    """
    DIALOGUE = "1WeQi-Qgsz1gyw7wVCD0bn4xokiZkEqa7"
    ARCHIVE = "1bKi-8WWi441y_CsBnMWK-LmNmo8alU8I"
    SYSTEM = "1sv3hSNGMT3qqLHbfWfe6Yy8odubVEqrb"





scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)

# intitialise l'autorisation
gc = gspread.authorize(credentials)


def get_matrice_sheet(nom_sheet):
    """renvoie la liste de liste de la première page du sheet en paramètre.
    chaque ligne dans la liste de liste sera aussi longue que la position de l'élément le plus éloigné dans la ligne du sheet

    Args:
        nom_sheet (str): nom du fichier google sheet

    Returns:
        list(list(str)): toutes les données présentes dans la sheet, placées aux mêmes positions que dans la sheet
    """
    max_retries = 100  # Nombre maximum de tentatives de requêtes
    wait_time = 5  # Temps d'attente en secondes entre les tentatives

    for i in range(max_retries):
        try:
            sheet = gc.open(nom_sheet).sheet1
        except:
            time.sleep(wait_time)
            continue
        try:
            return sheet.get()
        except:
            time.sleep(wait_time)


def get_liste_sheet_dossier(dossier):
    """renvoie la liste des sheet présent dans un dossier drive, dont le compte à accès

    Args:
        dossier (str): id du dossier (caractères dans l'url après folders\)

    Returns:
        list(dict): liste de dictionnaires avec id, name, createdTime, modifiedTime
    """
    max_retries = 100  # Nombre maximum de tentatives de requêtes
    wait_time = 5  # Temps d'attente en secondes entre les tentatives

    for i in range(max_retries):
        try:
            return gc.list_spreadsheet_files(folder_id=dossier)
        except:
            time.sleep(wait_time)
