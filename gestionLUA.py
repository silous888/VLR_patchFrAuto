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
        text = utils.remplace_e_aigue(text)
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
        text = utils.remplace_e_aigue(text)

        pattern = fr'{id}\s*=\s*"([^\n]+)"'
        contenu_modifie = re.sub(
            pattern,
            f'{id} = "{text}"',
            contenu_lua
        )
        contenu_lua = contenu_modifie

    with open(DOSSIER_LUA_DIALOGUE + nom_fichier, 'w', encoding='utf-8') as fichier:
        fichier.write(contenu_modifie)


def modifier_textes_dans_fichier_archive(nom_fichier, mat):
    for index in range(len(mat)):
        if len(mat[index][5]) == 0:
            continue
        if mat[index][4].startswith("archive"):
            archive_id = mat[index][4]
            new_title = mat[index][5]
            new_sentence = []
            it_new_arch = 1
            while (index + it_new_arch) < len(mat):
                if mat[index + it_new_arch][4].startswith("archive"):
                    break
                new_sentence.append(mat[index+it_new_arch][5])
                it_new_arch += 1

            total_length = 0
            final_string = ""
            for string in new_sentence:
                total_length += len(string)
            if total_length != 0:
                formatted_sentence = '",\n      "'.join(s.replace('"', r'\"').replace('\t', r'\t') for s in new_sentence)
                final_string = '"' + formatted_sentence + '"\n    '

            with open(DOSSIER_LUA_DIALOGUE + nom_fichier, "r", encoding='utf-8') as file:
                content = file.read()
            # Find the start and end indices of the specified archive ID
            start_index = content.find(archive_id)
            if start_index == -1:
                print("Archive ID not found.")
                return
            end_index = content.find("}", start_index) - 1
            if end_index == -1:
                print("End of archive not found.")
                return

            # Extract the archive content
            archive_content = content[start_index:end_index+1]

            # Update the title and sentence for the given ID
            title_index = archive_content.find("title")
            if title_index != -1:
                title_end_index = archive_content.find('",', title_index + 9)  # 9 is the length of "'title'"
                if title_end_index != -1:
                    updated_title = new_title
                    archive_content = archive_content[:title_index + 9] + updated_title + archive_content[title_end_index:-1]

            sentence_index = archive_content.find("sentence")
            if sentence_index != -1:
                sentence_start_index = sentence_index + 19
                sentence_end_index = end_index
                if sentence_start_index != -1 and sentence_end_index != -1:
                    if len(final_string) == 0:
                        archive_content = archive_content[:sentence_start_index-1] + "{" + archive_content[sentence_end_index+1:]
                    else:
                        archive_content = archive_content[:sentence_start_index] + final_string + archive_content[sentence_end_index+1:]

            # Update the content with the updated archive
            updated_content = content[:start_index] + archive_content + content[end_index+1:]

            with open(DOSSIER_LUA_DIALOGUE + nom_fichier, "w", encoding='utf-8') as file:
                file.write(updated_content)


def remplacer_texte(id_element, nouveau_texte, contenu_lua):
    lignes = contenu_lua.split('\n')
    for i, ligne in enumerate(lignes):
        if id_element in ligne:
            debut_texte = ligne.find('"') + 1
            fin_texte = ligne.rfind('"')
            if debut_texte != -1 and fin_texte != -1:
                lignes[i] = f'{ligne[:debut_texte]}{nouveau_texte}{ligne[fin_texte:]}'
    return '\n'.join(lignes)
