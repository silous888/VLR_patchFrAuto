from fileFolderUI import FileFolderUI
import sousMain as sm

# pyinstaller --onefile --noconsole --name VLR_Patch_Automatique --icon=./ressource/DreamteamLogo.ico main.py

def process(instance_worker):
    """fonction passée au l'instance de l'UI

    Args:
        instance_worker (worker): permet de modifier la valeur de la barre
        de progression, et le texte de progression
    """
    sm.update_texte_progression(instance_worker, "recherche et copie du bin zero escape")
    chemin_bin_steam = sm.recup_bin_ze_et_chemin_steam()

    sm.incrementer_progression(instance_worker, 10)
    sm.gestion_NOVEL(instance_worker)
    sm.gestion_ESCAPE(instance_worker)
    sm.gestion_SYSTEM(instance_worker)
    # sm.gestion_DESC(instance_worker)
    # sm.gestion_AUTRE(instance_worker)
    
    # # sm.gestion_images_PNG(instance_worker)
    # # sm.gestion_images_DDS(instance_worker)
    # # sm.gestion_videos(instance_worker)

    instance_worker.set_value_progressbar(90)
    sm.update_texte_progression(instance_worker, "recompilation du jeu")
    sm.recompiler_jeu(chemin_bin_steam)
    # sm.incrementer_progression(instance_worker, 10)


# -------------------- Main code -------------------
if __name__ == "__main__":
    var = FileFolderUI()
    var.process_func = lambda: process(var.get_worker())
    var.has_progressbar = True
    var.has_lineedit = False
    var.run()
