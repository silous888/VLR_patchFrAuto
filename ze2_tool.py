import subprocess


TOOL_VLR_PATH = "VLR_patch_data\\zevlr.exe "


def unpack_ze2_bin():
    """unpack bin of ze2"""
    command = [TOOL_VLR_PATH,
               "unpack"]
    subprocess.run(command,
                   shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW)


def generate_krlist():
    """generate krlist, for the font"""
    command = [TOOL_VLR_PATH,
               "krlist"]
    subprocess.run(command,
                   shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW)


def patch_files():
    """compile files in mod_dlg, compiled files will be in patch_res"""
    command = [TOOL_VLR_PATH,
               "patch"]
    subprocess.run(command,
                   shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW)


def repack_ze2_bin():
    """repack bin of VLR"""
    command = [TOOL_VLR_PATH,
               "repack"]
    subprocess.run(command,
                   shell=True,
                   creationflags=subprocess.CREATE_NO_WINDOW)
