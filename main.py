import sys

import sounddevice as sd
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from src.recording import recording


class Main(QMainWindow):
    MODELS_INTERFACE_BLOCK = ['model_type_box', 'rec_type_label']
    PC_SOUNDS_INTERFACE_BLOCK = ['rec_type_box', 'rec_type_label', 'start_btn', 'reg_seconds']
    FILES_INTERFACE_BLOCK = ['path_label', 'path_sound_label', 'path_btn']
    METHOD_PARAMETERS_BLOCK = ['reg_1', 'reg_label_1', 'reg_2', 'reg_label_2', 'reg_3', 'reg_label_3',
                               'reg_4', 'reg_label_4', 'reg_5', 'reg_label_5']

    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('styles/interface.ui', self)
        self.choise_event(0)
        self.path_btn.clicked.connect(self.getting_file_path)
        self.input_type_box.currentIndexChanged.connect(lambda: self.choise_event(0))
        self.rec_type_box.currentIndexChanged.connect(lambda: self.choise_event(1))
        self.start_btn.clicked.connect(lambda: recording(self.get_index(), self.reg_seconds.text()))

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
                self.graphics_btn.setGeometry(10, 395, 316, 30)
                self.rec_type_label.setText('Выберите аудиомодель:')
            elif self.input_type_box.currentText() == 'Файл':
                for box in self.PC_SOUNDS_INTERFACE_BLOCK, self.MODELS_INTERFACE_BLOCK, self.METHOD_PARAMETERS_BLOCK:
                    for item in box:
                        eval('self.' + item + '.hide()')
                for item in self.FILES_INTERFACE_BLOCK:
                    eval('self.' + item + '.show()')
                self.line_4.setGeometry(10, 195, 1, 110)
                self.line_5.setGeometry(325, 195, 1, 110)
                self.line_6.setGeometry(10, 305, 316, 1)
                self.graphics_btn.setGeometry(10, 310, 316, 30)
            else:
                for box in self.MODELS_INTERFACE_BLOCK, self.FILES_INTERFACE_BLOCK, self.METHOD_PARAMETERS_BLOCK:
                    for item in box:
                        eval('self.' + item + '.hide()')
                for item in self.PC_SOUNDS_INTERFACE_BLOCK:
                    eval('self.' + item + '.show()')
                self.line_4.setGeometry(10, 195, 1, 165)
                self.line_5.setGeometry(325, 195, 1, 165)
                self.line_6.setGeometry(10, 360, 316, 1)
                self.graphics_btn.setGeometry(10, 365, 316, 30)
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

    def get_index(self):
        devices = sd.query_devices()
        for dev in devices:
            if dev['name'] == self.input_type_box.currentText():
                return dev['name']


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    process = Main()
    process.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
