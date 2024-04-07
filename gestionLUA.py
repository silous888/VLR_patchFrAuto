import re
import utils


DOSSIER_LUA_DIALOGUE = "VLR_patch_data\\mod_dlg\\"


def modifier_texte_dans_fichier(nom_fichier, mat):

    # utils.logging.error(DOSSIER_LUA_DIALOGUE + nom_fichier + " on est lecture")
    with open(DOSSIER_LUA_DIALOGUE + nom_fichier, 'r', encoding='utf-8') as fichier:
        # utils.logging.error(DOSSIER_LUA_DIALOGUE + nom_fichier + " on est lecture 2")
        contenu_lua = fichier.read()
        # utils.logging.error(DOSSIER_LUA_DIALOGUE + nom_fichier + " on est lecture 3")

    for index in range(len(mat)):
        # utils.logging.error(DOSSIER_LUA_DIALOGUE + nom_fichier + " on est " + str(index))
        id = mat[index][0]
        name = mat[index][1]
        text = utils.remplace_guillemet(mat[index][3])

        pattern = fr'{id}\s*=\s*{{[^}}]+}}'

        contenu_modifie = re.sub(
            pattern,
            f'{id} = {{name = "{name}", text = "{text}"}}',
            contenu_lua
        )
        contenu_lua = contenu_modifie

    with open(DOSSIER_LUA_DIALOGUE + nom_fichier, 'w', encoding='utf-8') as fichier:
        # utils.logging.error(DOSSIER_LUA_DIALOGUE + nom_fichier + " on est ecriture")
        fichier.write(contenu_modifie)


def modifier_texte_dans_fichier_system(nom_fichier, mat):

    with open(DOSSIER_LUA_DIALOGUE + nom_fichier, 'r', encoding='utf-8') as fichier:
        contenu_lua = fichier.read()

    for index in range(len(mat)):

        id = mat[index][0]
        text = utils.remplace_guillemet(mat[index][3])

        pattern = fr'{id}\s*=\s*"([^\n]+)"'
        contenu_modifie = re.sub(
            pattern,
            f'{id} = "{text}"',
            contenu_lua
        )
        contenu_lua = contenu_modifie

    with open(DOSSIER_LUA_DIALOGUE + nom_fichier, 'w', encoding='utf-8') as fichier:
        fichier.write(contenu_modifie)


def remplacer_texte(id_element, nouveau_texte, contenu_lua):
    lignes = contenu_lua.split('\n')
    for i, ligne in enumerate(lignes):
        if id_element in ligne:
            debut_texte = ligne.find('"') + 1
            fin_texte = ligne.rfind('"')
            if debut_texte != -1 and fin_texte != -1:
                lignes[i] = f'{ligne[:debut_texte]}{nouveau_texte}{ligne[fin_texte:]}'
    return '\n'.join(lignes)
