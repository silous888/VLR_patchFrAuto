# -------------------- Import Lib Standard -------------------
import sys
import os
import inspect
import time

# -------------------- Import Lib Tier -------------------
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QProgressBar
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QDir, QObject, QThread, QRect, QSize, Qt

# -------------------- Import Lib User -------------------
from Ui_ihm import Ui_MainWindow

from uiChoixFichierPatch import CheckboxWindowFile
from uiChoixImagePatch import CheckboxWindowImage
from utils import etats_liste
# -------------------- Constant -------------------



# -------------------- Class -------------------


class FileExtensions:
    VIDEOS = [".mp4", ".m4v", ".avi", ".mov", ".wmv"]
    PICTURES = [".jpg", ".png", ".bmp", ".gif", ".tiff"]
    DOCUMENTS = [".pdf", ".docx", ".txt", ".rtf"]
    AUDIO = [".mp3", ".wav", ".ogg", ".flac"]
    SPREADSHEETS = [".csv", ".xlsx", ".ods"]
    ARCHIVES = [".zip", ".rar", ".7z", ".tar.gz"]
    PROGRAMS = [".exe", ".msi"]
    SCRIPTS = [".py", ".sh", ".bat"]
    FONT_FILES = [".ttf", ".otf"]
    WEB_FILES = [".html", ".css", ".js"]


# -------------------- Functions -------------------


def _do_nothing1():
    pass

def _do_nothing2(str_var):
    pass

def _do_nothing3(str_var, list_str_var):
    pass



# -------------------------------------------------------------------#
#                          CLASS WORKER                              #
# -------------------------------------------------------------------#
class _Worker(QObject):
    """Class for thread
    put the process in a thread and send a signal when the process
    is finished
    """
    command = pyqtSignal(str, list)
    signal_process_done = pyqtSignal()
    signal_set_value_progressbar = pyqtSignal(int)
    signal_set_text_progress = pyqtSignal(str)
    signal_listes_fichiers_bool = pyqtSignal(list)
    signal_listes_images_bool = pyqtSignal(list)
    
    tailles = [16, 54, 8]
    tailles_images = [9, 6, 5, 10, 10, 4, 9, 3, 9, 4]
    # Initialiser la liste principale
    liste_choix_fichiers = []
    liste_choix_images = []
    choix_patch_dds = False
    choix_patch_videos = False

    def __init__(self):
        super().__init__()
        self.change_etats_fichiers(True)
        self.change_etats_images(False)
        self.process_func1 = _do_nothing1
        self.process_func2 = _do_nothing2
        self.process_func3 = _do_nothing3
        # Boucle pour créer les listes intérieures et les remplir de valeurs True

    @pyqtSlot(str, list)
    def thread_process(self, path_and_folder_name, list_elements=None):
        self.process_func1()
        self.process_func2(path_and_folder_name)
        self.process_func3(path_and_folder_name, list_elements)

        self.signal_process_done.emit()

    def change_etats_fichiers(self, boolVal):
        self.liste_choix_fichiers = []
        for taille in self.tailles:
            liste_interieure = [boolVal] * taille
            self.liste_choix_fichiers.append(liste_interieure)
    
    def change_etats_images(self, boolVal):
        self.liste_choix_images = []
        for taille in self.tailles_images:
            liste_interieure = [boolVal] * taille
            self.liste_choix_images.append(liste_interieure)
            
    def set_value_progressbar(self, value):
        self.signal_set_value_progressbar.emit(value)

    def set_text_progress(self, text):
        self.signal_set_text_progress.emit(text)
    
    def set_choix_fichiers_bool(self, liste):
        self.liste_choix_fichiers = liste
        
    def set_choix_images_bool(self, liste):
        self.liste_choix_images = liste




# -------------------------------------------------------------------#
#                         CLASS MAINWINDOW                           #
# -------------------------------------------------------------------#
class _MainWindow(QMainWindow):
    """class of the window"""
    def __init__(self):
        super(_MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_done.hide()
        self.ui.label_process.hide()

        self.m_thread = QThread()
        self.m_thread.start()
        self.m_worker = _Worker()
        self.m_worker.moveToThread(self.m_thread)

        self.progress_bar = QProgressBar(self.ui.centralwidget)
        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(0)
        self.progress_bar.setGeometry(QRect(30, 10, 536, 20))
        self.progress_bar.hide()

        self.set_up_connect()

    def set_up_connect(self):
        """Connect every signals"""
        # signals of the ui
        self.ui.pushButton_browse.clicked.connect(self.find_element)
        self.ui.pushButton_process.clicked.connect(self.run_process)
        self.ui.pushButton_choix_fichier.clicked.connect(self.ouvrir_choix_fichier)
        self.ui.pushButton_choix_image.clicked.connect(self.ouvrir_choix_image)
        self.ui.fileEdit_path.textChanged.connect(self.hide_done)
        self.ui.checkBox_fichiers.clicked.connect(self.update_tous_les_fichiers)
        self.ui.checkBox_images.clicked.connect(self.update_toutes_les_images)
        self.ui.checkBox_imagesDDS.clicked.connect(self.update_toutes_les_imagesDDS)
        self.ui.checkBox_videos.clicked.connect(self.update_toutes_les_videos)
        # signals of the thread
        self.m_worker.command.connect(self.m_worker.thread_process)
        self.m_worker.signal_listes_fichiers_bool.connect(self.m_worker.set_choix_fichiers_bool)
        self.m_worker.signal_listes_images_bool.connect(self.m_worker.set_choix_images_bool)
        self.m_worker.signal_process_done.connect(self.enable_ui)
        self.m_worker.signal_set_value_progressbar.connect(self.change_progressbar_value)
        self.m_worker.signal_set_text_progress.connect(self.change_progress_text)

    def define_attribute(self, is_folder, has_lineedit, has_progressbar, files_extension, process_func):
        self.is_folder = is_folder
        self.files_extension = files_extension
        self.files_extension_uppercase = [x.upper() for x in self.files_extension]
        self.has_lineedit = has_lineedit
        self.has_progressbar = has_progressbar
        num_args = len(inspect.getfullargspec(process_func).args)
        if num_args == 0:
            self.m_worker.process_func1 = process_func
            self.m_worker.process_func2 = _do_nothing2
            self.m_worker.process_func3 = _do_nothing3
        if num_args == 1:
            self.m_worker.process_func2 = process_func
            self.m_worker.process_func1 = _do_nothing1
            self.m_worker.process_func3 = _do_nothing3
        if num_args == 2:
            self.m_worker.process_func3 = process_func
            self.m_worker.process_func1 = _do_nothing1
            self.m_worker.process_func2 = _do_nothing2


    def update_ui(self):
        if self.has_progressbar:
            self.progress_bar.show()
        if not self.has_lineedit:
            self.ui.fileEdit_path.hide()
            self.ui.pushButton_browse.hide()
        if self.has_lineedit and self.has_progressbar:
            self.setMinimumSize(QSize(642, 116))
            self.setMaximumSize(QSize(642, 116))
            self.progress_bar.setGeometry(QRect(30, 45, 536, 20))
            self.ui.pushButton_process.setGeometry(QRect(240, 70, 75, 23))
            self.ui.label_done.setGeometry(QRect(330, 70, 51, 20))
            self.ui.label_process.setGeometry(QRect(330, 70, 131, 21))


    def adapt_const_extention_filter(self):
        """adapt extension put in files_extension to the format of the filter of GetOpenFileName"""
        filter = "Files ("
        extensions = " ".join(f"*{ext}" for ext in self.files_extension)
        filter = filter + extensions + ")"
        return filter

    @pyqtSlot()
    def find_element(self):
        """open the finder windows,
        put the path in the fileEdit
        """
        if self.is_folder:
            folder = QFileDialog.getExistingDirectory(self, "Choose folder",
                                                    QDir.currentPath(), QFileDialog.ShowDirsOnly)
            self.ui.fileEdit_path.setText(folder)
        else:

            file, _ = QFileDialog.getOpenFileName(self, "Choose file",
                                                     QDir.currentPath(),
                                                     filter=self.adapt_const_extention_filter())
            self.ui.fileEdit_path.setText(file)

    @pyqtSlot()
    def run_process(self):
        """call  the process thread"""
        if not self.has_lineedit:
            self.disable_ui()
            self.m_worker.command.emit("", [])
        elif self.is_folder:
            folder = self.ui.fileEdit_path.text()
            if os.path.isdir(folder):
                data = [f for f in os.listdir(folder) if f.endswith(tuple(self.files_extension + self.files_extension_uppercase))]
                if len(data) !=0:
                    self.disable_ui()
                    self.m_worker.command.emit(folder, data)
        else:
            file = self.ui.fileEdit_path.text()
            if file.endswith(tuple(self.files_extension + self.files_extension_uppercase)) and os.path.exists(file):
                self.disable_ui()
                self.m_worker.command.emit(file, [])

    @pyqtSlot()
    def ouvrir_choix_fichier(self):
        window_fichier = CheckboxWindowFile()
        window_fichier.exec_()
        checkbox_values = window_fichier.get_checkbox_values()
        self.m_worker.signal_listes_fichiers_bool.emit(checkbox_values)
        time.sleep(0.3)
        self.change_etats_checkbox_fichiers(self.m_worker.liste_choix_fichiers)

    @pyqtSlot()
    def ouvrir_choix_image(self):
        window_images = CheckboxWindowImage()
        window_images.exec_()
        checkbox_values_images = window_images.get_checkbox_values()
        self.m_worker.signal_listes_images_bool.emit(checkbox_values_images)
        time.sleep(0.3)
        self.change_etats_checkbox_images(self.m_worker.liste_choix_images)
    
    @pyqtSlot()
    def update_tous_les_fichiers(self):
        self.m_worker.change_etats_fichiers(self.ui.checkBox_fichiers.isChecked())

    @pyqtSlot()
    def update_toutes_les_images(self):
        self.m_worker.change_etats_images(self.ui.checkBox_images.isChecked())
    
    @pyqtSlot()
    def update_toutes_les_imagesDDS(self):
        self.m_worker.choix_patch_dds = self.ui.checkBox_imagesDDS.isChecked()

    @pyqtSlot()
    def update_toutes_les_videos(self):
        self.m_worker.choix_patch_videos = self.ui.checkBox_videos.isChecked()

    def change_etats_checkbox_fichiers(self, liste):
        etat = etats_liste(liste)
        if etat == 1:
            self.ui.checkBox_fichiers.setCheckState(Qt.CheckState.Checked)
        if etat == 0:
            self.ui.checkBox_fichiers.setCheckState(Qt.CheckState.PartiallyChecked)
        if etat == -1:
            self.ui.checkBox_fichiers.setCheckState(Qt.CheckState.Unchecked)
    
    def change_etats_checkbox_images(self, liste):
        etat = etats_liste(liste)
        if etat == 1:
            self.ui.checkBox_images.setCheckState(Qt.CheckState.Checked)
        if etat == 0:
            self.ui.checkBox_images.setCheckState(Qt.CheckState.PartiallyChecked)
        if etat == -1:
            self.ui.checkBox_images.setCheckState(Qt.CheckState.Unchecked)

    @pyqtSlot(str)
    def hide_done(self, text):
        """hide the label "done", call when the path change

        Attrs:
        - text (str): not used, but send by the signal of fileEdit
        """
        self.ui.label_done.hide()

    @pyqtSlot()
    def enable_ui(self):
        """enable ui when process is done"""
        self.ui.checkBox_fichiers.setEnabled(True)
        self.ui.checkBox_images.setEnabled(True)
        self.ui.checkBox_imagesDDS.setEnabled(True)
        self.ui.checkBox_videos.setEnabled(True)
        self.ui.label_process.hide()
        self.ui.label_done.show()
        self.ui.pushButton_process.setEnabled(True)
        self.ui.pushButton_choix_fichier.setEnabled(True)
        self.ui.pushButton_choix_image.setEnabled(True)
        self.ui.pushButton_browse.setEnabled(True)
        self.ui.fileEdit_path.setEnabled(True)
        self.ui.label_process.text = "in process..."
        self.progress_bar.setValue(0)

    def disable_ui(self):
        """disable ui during the process"""
        self.ui.checkBox_fichiers.setEnabled(False)
        self.ui.checkBox_images.setEnabled(False)
        self.ui.checkBox_imagesDDS.setEnabled(False)
        self.ui.checkBox_videos.setEnabled(False)
        self.ui.label_process.show()
        self.ui.label_done.hide()
        self.ui.pushButton_process.setEnabled(False)
        self.ui.pushButton_choix_fichier.setEnabled(False)
        self.ui.pushButton_choix_image.setEnabled(False)
        self.ui.pushButton_browse.setEnabled(False)
        self.ui.fileEdit_path.setEnabled(False)

    @pyqtSlot(int)
    def change_progressbar_value(self, value):
        self.progress_bar.setValue(value)

    @pyqtSlot(str)
    def change_progress_text(self, text):
        self.ui.label_process.setText(text)







class FileFolderUI():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = _MainWindow()
        
        self.has_lineedit = True
        self.has_progressbar = False
        self.is_folder = True
        self.files_extension = FileExtensions.DOCUMENTS
        self.process_func = _do_nothing1
        self.window.define_attribute(self.is_folder, self.has_lineedit, self.has_progressbar, self.files_extension, self.process_func)

    def run(self):
        self.window.define_attribute(self.is_folder, self.has_lineedit, self.has_progressbar, self.files_extension, self.process_func)
        self.window.update_ui()
        self.window.show()
        sys.exit(self.app.exec())

    def get_worker(self):
        return self.window.m_worker

