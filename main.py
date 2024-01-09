from fileFolderUI import FileFolderUI
import submain

# pyinstaller --onefile --noconsole --name VLR_Patch_Auto --icon=./ressource/DreamteamLogo.ico main.py


def process(instance_worker):
    """function send as parameter of the instance of the UI

    Args:
        instance_worker (worker): to change progress bar and progress text
    """
    submain.get_bin_vlr()

    # sm.gestion_NOVEL(instance_worker)
    # sm.gestion_ESCAPE(instance_worker)
    # sm.gestion_SYSTEM(instance_worker)
    # sm.gestion_DESC(instance_worker)
    # sm.gestion_AUTRE(instance_worker)

    # # sm.gestion_images_PNG(instance_worker)
    # # sm.gestion_images_DDS(instance_worker)
    # # sm.gestion_videos(instance_worker)

    # instance_worker.set_value_progressbar(90)
    # sm.update_texte_progression(instance_worker, "recompilation du jeu")
    # sm.recompiler_jeu(chemin_bin_steam)
    # sm.incrementer_progression(instance_worker, 10)


# -------------------- Main code -------------------
if __name__ == "__main__":
    var = FileFolderUI()
    var.process_func = lambda: process(var.get_worker())
    var.has_progressbar = True
    var.has_lineedit = False
    var.run()
