import subprocess


tool_vlr = "VLR_patch_data\\zevlr.exe "

def unpack_ze2_bin():
    """décompile le bin de vlr"""
    subprocess.run(
        tool_vlr + "unpack",
        shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
    )

def creation_krlist():
    """fait le fichier krlist de font"""
    subprocess.run(
        tool_vlr + "krlist",
        shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
    )

def patch_fichiers():
    """transforme les fichiers dans mod_dlg et fichiers compréhensibles pour le jeu,
    et les mets dans patch_res"""
    subprocess.run(
        tool_vlr + "patch",
        shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
    )

def repack_ze2_bin():
    """repack le bin de vlr"""
    subprocess.run(
        tool_vlr + "repack",
        shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
    )

