import shutil
import sqlite3
import sys
import os

import sounddevice as sd
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from src.recording import recording
from src.spectrogram import draw_spectrogram
from src.waveform import draw_waveform


class MainWindow(QMainWindow):
    def __init__(self):
        try:
            super(MainWindow, self).__init__()
            uic.loadUi('styles/main_window.ui', self)

            self.reference_window = None
            self.analyse_window = None

            self.create_reference_btn.clicked.connect(lambda: self.initialization_window(0))
            self.analyse_btn.clicked.connect(lambda: self.initialization_window(1))
        except Exception as e:
            print('Ошибка 0: Ошибка при инициализации окна.')
            print(e)

    def initialization_window(self, id):
        try:
            if id == 0:
                if self.reference_window is None:
                    self.reference_window = ReferenceWindow(parent=self)
                self.reference_window.show()
                self.reference_window.raise_()
                self.reference_window.activateWindow()
            else:
                if self.analyse_window is None:
                    self.analyse_window = AnalyseWindow(parent=self)
                self.analyse_window.show()
                self.analyse_window.raise_()
                self.analyse_window.activateWindow()
        except Exception as e:
            print('Ошибка 0: Ошибка при инициализации окна.')
            print(e)


class AnalyseWindow(QWidget):
    def __init__(self, parent=None):
        try:
            self.parent_window = parent
            super(AnalyseWindow, self).__init__()
            uic.loadUi('styles/analyse_window.ui', self)
            self.path_analyse_btn.clicked.connect(lambda: self.get_file_path_analyse())
            self.analyse_btn.clicked.connect(lambda: self.analyse())
            conn = sqlite3.connect('references/graphs.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM reference ORDER BY name")
            groups = cursor.fetchall()
            self.reference_box.clear()
            for (name,) in groups:
                self.reference_box.addItem(name)
        except Exception as e:
            print('Ошибка 0: Ошибка при инициализации окна.')
            print(e)

    def analyse(self):
        try:
            conn = sqlite3.connect('references/graphs.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM reference WHERE name = ?", (self.reference_box.currentText(),))
            result = cursor.fetchone()
            group_id = result[0]
            cursor.execute("SELECT type, path FROM ref_graphs WHERE ref_graphs_id = ?", (group_id,))
            graphs = cursor.fetchall()
            if self.type_box.currentText() == 'Амплитудный':
                for item in graphs:
                    if item[0] == 'amplitude':
                        self.reference_gph.setPixmap(QPixmap(item[1]))
                self.analyse_gph.setPixmap(QPixmap(draw_waveform(self.path_analyse_label.text())))
            else:
                for item in graphs:
                    if item[0] == 'spectrum':
                        self.reference_gph.setPixmap(QPixmap(item[1]))
                self.analyse_gph.setPixmap(QPixmap(draw_spectrogram(self.path_analyse_label.text())))
        except Exception as e:
            print('Ошибка 1Е: Ошибка исполнения функции analyse.')
            print(e)

    def get_file_path_analyse(self):
        try:
            self.path_analyse_label.setText(QtWidgets.QFileDialog.getOpenFileName()[0])
        except Exception as e:
            print('Ошибка 1Ё: Ошибка исполнения функции get_file_path_analyse.')
            print(e)


class ReferenceWindow(QWidget):
    MODELS_INTERFACE_BLOCK = ['model_type_box', 'rec_type_label']
    PC_SOUNDS_INTERFACE_BLOCK = ['rec_type_box', 'rec_type_label', 'start_btn', 'reg_seconds']
    FILES_INTERFACE_BLOCK = ['path_label', 'path_sound_label', 'path_btn']
    METHOD_PARAMETERS_BLOCK = ['reg_1', 'reg_label_1', 'reg_2', 'reg_label_2', 'reg_3', 'reg_label_3',
                               'reg_4', 'reg_label_4', 'reg_5', 'reg_label_5']
    PATH_SPECTRUM = None
    PATH_WAVEFORM = None
    def __init__(self, parent=None):
        try:
            self.parent_window = parent
            super(ReferenceWindow, self).__init__()
            uic.loadUi('styles/reference_window.ui', self)
            try:
                os.mkdir('tmp')
            except:
                pass
            self.choise_event(0)
            self.path_btn.clicked.connect(lambda: self.get_file_path())
            self.input_type_box.currentIndexChanged.connect(lambda: self.choise_event(0))
            self.rec_type_box.currentIndexChanged.connect(lambda: self.choise_event(1))
            self.start_btn.clicked.connect(lambda: self.path_sound_label.setText(recording(self.get_index(),
                                                                                           self.reg_seconds.text())))
            self.graphics_btn.clicked.connect(lambda: self.drawing())
            self.save_btn.clicked.connect(lambda: self.saving())
        except Exception as e:
            print('Ошибка 0: Ошибка при инициализации окна.')
            print(e)

    def choise_event(self, box_id):
        try:
            if box_id == 0:
                if self.input_type_box.currentText() == 'Аудиомодель':
                    for box in self.PC_SOUNDS_INTERFACE_BLOCK, self.FILES_INTERFACE_BLOCK:
                        for item in box:
                            eval('self.' + item + '.hide()')
                    for box in self.MODELS_INTERFACE_BLOCK, self.METHOD_PARAMETERS_BLOCK:
                        for item in box:
                            eval('self.' + item + '.show()')
                    self.line_4.setGeometry(10, 195, 1, 195)
                    self.line_5.setGeometry(325, 195, 1, 195)
                    self.line_6.setGeometry(10, 390, 316, 1)
                    self.graphics_btn.setGeometry(10, 390, 316, 30)
                    self.rec_type_label.setText('Выберите аудиомодель:')
                elif self.input_type_box.currentText() == 'Файл':
                    for box in self.PC_SOUNDS_INTERFACE_BLOCK, self.MODELS_INTERFACE_BLOCK, self.METHOD_PARAMETERS_BLOCK:
                        for item in box:
                            eval('self.' + item + '.hide()')
                    for item in self.FILES_INTERFACE_BLOCK:
                        eval('self.' + item + '.show()')
                    self.line_4.setGeometry(10, 195, 1, 105)
                    self.line_5.setGeometry(325, 195, 1, 105)
                    self.line_6.setGeometry(10, 300, 316, 1)
                    self.graphics_btn.setGeometry(10, 300, 316, 30)
                else:
                    for box in self.MODELS_INTERFACE_BLOCK, self.FILES_INTERFACE_BLOCK, self.METHOD_PARAMETERS_BLOCK:
                        for item in box:
                            eval('self.' + item + '.hide()')
                    for item in self.PC_SOUNDS_INTERFACE_BLOCK:
                        eval('self.' + item + '.show()')
                    self.line_4.setGeometry(10, 195, 1, 165)
                    self.line_5.setGeometry(325, 195, 1, 165)
                    self.line_6.setGeometry(10, 360, 316, 1)
                    self.graphics_btn.setGeometry(10, 360, 316, 30)
                    self.rec_type_label.setText('Выберите устройство записи:')
                    self.choise_event(1)
            elif box_id == 1:
                devices = sd.query_devices()
                for dev in devices:
                    if dev['max_input_channels'] >= 1 and self.rec_type_box.findText(dev['name']) == -1:
                        self.rec_type_box.addItem(dev['name'])

            else:
                if self.model_type_box.currentText() == 'a(t) = Acos(ωt + φ)':
                    pass
                else:
                    pass
        except Exception as e:
            print('Ошибка 1А: Ошибка исполнения функции choise_event.')
            print(e)

    def get_index(self):
        try:
            devices = sd.query_devices()
            for dev in devices:
                if dev['name'] == self.input_type_box.currentText():
                    return dev['name']
        except Exception as e:
            print('Ошибка 1Б: Ошибка исполнения функции get_index.')
            print(e)


    def get_file_path(self):
        try:
            self.path_sound_label.setText(QtWidgets.QFileDialog.getOpenFileName()[0])
        except Exception as e:
            print('Ошибка 1В: Ошибка исполнения функции get_file_path.')
            print(e)

    def drawing(self):
        try:
            self.PATH_SPECTRUM = draw_spectrogram(self.path_sound_label.text())
            self.PATH_WAVEFORM = draw_waveform(self.path_sound_label.text())
            self.specturm_gph.setPixmap(QPixmap(self.PATH_SPECTRUM))
            self.waveform_gph.setPixmap(QPixmap(self.PATH_WAVEFORM))
        except Exception as e:
            print('Ошибка 1Г: Ошибка исполнения функции drawing.')
            print(e)

    def saving(self):
        try:
            conn = sqlite3.connect('references/graphs.db')
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO reference (name) VALUES (?)", (self.reg_name.text(),))
            conn.commit()
            cursor.execute("SELECT id FROM reference WHERE name = ?", (self.reg_name.text(),))
            reference_id = cursor.fetchone()[0]
            shutil.copy(self.PATH_SPECTRUM, f'references/spectrum_{reference_id}.png')
            shutil.copy(self.PATH_WAVEFORM, f'references/waveform_{reference_id}.png')
            cursor.execute("INSERT INTO ref_graphs (ref_graphs_id, type, path) VALUES (?, ?, ?)",
                           (reference_id, 'spectrum', f'references/spectrum_{reference_id}.png'))
            cursor.execute("INSERT INTO ref_graphs (ref_graphs_id, type, path) VALUES (?, ?, ?)",
                           (reference_id, 'amplitude', f'references/waveform_{reference_id}.png'))
            conn.commit()
        except Exception as e:
            print('Ошибка 1Д: Ошибка исполнения функции saving.')
            print(e)



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    process = MainWindow()
    process.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())