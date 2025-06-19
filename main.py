import shutil
import sys
import os

import sounddevice as sd
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from src.frequency_spectrum import draw_frequency_spectrum
from src.recording import recording
from src.spectrogram import draw_spectrogram
from src.waveform import draw_waveform


class Main(QMainWindow):
    MODELS_INTERFACE_BLOCK = ['model_type_box', 'rec_type_label']
    PC_SOUNDS_INTERFACE_BLOCK = ['rec_type_box', 'rec_type_label', 'start_btn', 'reg_seconds']
    FILES_INTERFACE_BLOCK = ['path_label', 'path_sound_label', 'path_btn']
    METHOD_PARAMETERS_BLOCK = ['reg_1', 'reg_label_1', 'reg_2', 'reg_label_2', 'reg_3', 'reg_label_3',
                               'reg_4', 'reg_label_4', 'reg_5', 'reg_label_5']

    def __init__(self):
        self.path = None
        try:
            super(Main, self).__init__()
            uic.loadUi('styles/interface.ui', self)
            self.graph_window = None
            try:
                os.mkdir('tmp')
            except:
                pass
            self.choise_event(0)
            self.path_btn.clicked.connect(self.getting_file_path)
            self.input_type_box.currentIndexChanged.connect(lambda: self.choise_event(0))
            self.rec_type_box.currentIndexChanged.connect(lambda: self.choise_event(1))
            self.start_btn.clicked.connect(lambda: self.path_sound_label.setText(recording(self.get_index(),
                                                                                       self.reg_seconds.text())))
            self.graphics_btn.clicked.connect(lambda: self.drawing())
        except Exception as e:
            print(f'Ошибка запуска основного окна: {e}')

    def getting_file_path(self):
        self.path_sound_label.setText(QtWidgets.QFileDialog.getOpenFileName()[0])

    def choise_event(self, box_id):
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
                self.graphics_btn.setGeometry(10, 510, 316, 30)
                self.rec_type_label.setText('Выберите аудиомодель:')
                self.line_7.setGeometry(10, 400, 316, 1)
                self.line_8.setGeometry(10, 400, 1, 110)
                self.line_9.setGeometry(325, 400, 1, 110)
                self.line_10.setGeometry(10, 510, 316, 1)
                self.sopt_label_3.setGeometry(2, 395, 330, 25)
                self.output_type_label.setGeometry(2, 415, 330, 25)
                self.output_type_box.setGeometry(15, 440, 305, 50)
            elif self.input_type_box.currentText() == 'Файл':
                for box in self.PC_SOUNDS_INTERFACE_BLOCK, self.MODELS_INTERFACE_BLOCK, self.METHOD_PARAMETERS_BLOCK:
                    for item in box:
                        eval('self.' + item + '.hide()')
                for item in self.FILES_INTERFACE_BLOCK:
                    eval('self.' + item + '.show()')
                self.line_4.setGeometry(10, 195, 1, 75)
                self.line_5.setGeometry(325, 195, 1, 75)
                self.line_6.setGeometry(10, 270, 316, 1)
                self.graphics_btn.setGeometry(10, 415, 316, 30)
                self.line_7.setGeometry(10, 305, 316, 1)
                self.line_8.setGeometry(10, 305, 1, 105)
                self.line_9.setGeometry(325, 305, 1, 105)
                self.line_10.setGeometry(10, 410, 316, 1)
                self.sopt_label_3.setGeometry(2, 295, 330, 25)
                self.output_type_label.setGeometry(2, 315, 330, 25)
                self.output_type_box.setGeometry(15, 340, 305, 50)
            else:
                for box in self.MODELS_INTERFACE_BLOCK, self.FILES_INTERFACE_BLOCK, self.METHOD_PARAMETERS_BLOCK:
                    for item in box:
                        eval('self.' + item + '.hide()')
                for item in self.PC_SOUNDS_INTERFACE_BLOCK:
                    eval('self.' + item + '.show()')
                self.line_4.setGeometry(10, 195, 1, 165)
                self.line_5.setGeometry(325, 195, 1, 165)
                self.line_6.setGeometry(10, 360, 316, 1)
                self.graphics_btn.setGeometry(10, 485, 316, 30)
                self.rec_type_label.setText('Выберите устройство записи:')
                self.line_7.setGeometry(10, 375, 316, 1)
                self.line_8.setGeometry(10, 375, 1, 105)
                self.line_9.setGeometry(325, 375, 1, 105)
                self.line_10.setGeometry(10, 480, 316, 1)
                self.sopt_label_3.setGeometry(2, 365, 330, 25)
                self.output_type_label.setGeometry(2, 385, 330, 25)
                self.output_type_box.setGeometry(15, 410, 305, 50)
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


    def get_index(self):
        devices = sd.query_devices()
        for dev in devices:
            if dev['name'] == self.input_type_box.currentText():
                return dev['name']

    def drawing(self):
        if self.graph_window is None:
            self.graph_window = GraphWindow(parent=self)
        self.graph_window.show()
        self.graph_window.raise_()
        self.graph_window.activateWindow()
        if self.output_type_box.currentText() == 'Амплитудный график':
            self.path = draw_waveform(self.path_sound_label.text())
        elif self.output_type_box.currentText() == 'Спектрограмма':
            self.path = draw_spectrogram(self.path_sound_label.text())
        else:
            self.path = draw_frequency_spectrum(self.path_sound_label.text())
        self.graph_window.graph.setPixmap(QPixmap(self.path))


class GraphWindow(QWidget):
    def __init__(self, parent=None):
        self.parent_window = parent
        super(GraphWindow, self).__init__()
        uic.loadUi('styles/graph.ui', self)

        self.save_btn.clicked.connect(lambda: self.save_graph())

    def save_graph(self):
        main = Main()
        target_path, _ = QFileDialog.getSaveFileName(
            self,
            'Сохранить как...',
            'Graph.png',
            'PNG файлы (*.png);;Все файлы (*)'
        )
        if target_path:
            try:
                shutil.copy(self.parent_window.path, target_path)
            except Exception as e:
                print(f'Ошибка при копировании: {e}')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    process = Main()
    process.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
