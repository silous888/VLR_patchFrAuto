from fileFolderUI import FileFolderUI
import submain
from API import steam_game_api

# pyinstaller --onefile --noconsole --name VLR_Patch_Auto --icon=./ressource/DreamteamLogo.ico main.py


def process(instance_worker):
    """function send as parameter of the instance of the UI

    Args:
        instance_worker (worker): to change progress bar and progress text
    """
    submain.update_text_progression(instance_worker, "récupération bin du jeu")
    submain.get_bin_vlr()
    submain.gestion_NOVEL(instance_worker)
    # sm.gestion_ESCAPE(instance_worker)
    # sm.gestion_SYSTEM(instance_worker)
    # sm.gestion_DESC(instance_worker)
    # sm.gestion_AUTRE(instance_worker)

    # # sm.gestion_images_PNG(instance_worker)
    # # sm.gestion_images_DDS(instance_worker)
    # # sm.gestion_videos(instance_worker)

    instance_worker.set_value_progressbar(90)
    submain.update_text_progression(instance_worker, "recompilation du jeu")
    submain.compile_game(steam_game_api.find_game_path("Zero Escape The Nonary Games") + "ze2_data_jp.bin")
    submain.incrementer_progression(instance_worker, 10)


# -------------------- Main code -------------------
if __name__ == "__main__":
    var = FileFolderUI()
    var.process_func = lambda: process(var.get_worker())
    var.has_progressbar = True
    var.has_lineedit = False
    var.run()
