import API.steam_game_api as steamGameAPI

import os


def get_bin_vlr():
    if not os.path.exists(".\\VLR_patch_data\\org_bin\\ze2_data_jp.bin"):
        steamGameAPI.copy_data_from_steam_game_folder("Zero Escape The Nonary Games",
                                                      ".\\VLR_patch_data\\org_bin\\",
                                                      data_to_copy="ze2_data_jp.bin",
                                                      overwrite=False)
