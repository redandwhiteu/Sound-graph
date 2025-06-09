import sys


import pyaudio
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic


class Main(QMainWindow):
    def __init__(self):
        """
        Initialized program.
        """
        super(Main, self).__init__()
        uic.loadUi('mainUI.ui', self)

        # Visual.
        self.input_type.setEditable(True)
        self.input_type.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.input_type.lineEdit().setFont(QtGui.QFont('Roboto Slab', 12))
        self.input_type.lineEdit()
        self.input_type.lineEdit().setReadOnly(True)

        # Connect interfaceses with functions.
        self.path.clicked.connect(self.get_path)
        self.input_type.currentIndexChanged.connect(self.choise_changed)
        self.mic_type.currentIndexChanged.connect(self.choise_mic)

        #Hiding options.
        self.mic_ins.hide()
        self.mic_type.hide()
        self.start_sound.hide()
        self.stop_sound.hide()
        self.line_6.hide()
        self.line_7.hide()
        self.line_8.hide()

    def get_path(self):
        # Getting file
        path = QtWidgets.QFileDialog.getOpenFileName()
        self.path_ch_text.setText(path[0])

    def choise_changed(self):
        if self.input_type.currentText() == 'Файл':
            self.start_sound.hide()
            self.stop_sound.hide()
            self.mic_ins.hide()
            self.mic_type.hide()
            self.path.show()
            self.path_ch_text.show()
            self.path_text.show()
            self.line_5.show()
            self.line_6.hide()
            self.line_7.hide()
            self.line_8.hide()
            self.start_graphing.setGeometry(10, 300, 316, 30)
        elif self.input_type.currentText() == 'Звуки устройства':
            self.path.hide()
            self.path_ch_text.hide()
            self.path_text.hide()
            self.line_5.hide()
            self.line_6.show()
            self.line_7.show()
            self.line_8.show()
            self.start_sound.show()
            self.stop_sound.show()
            self.mic_ins.show()
            self.mic_type.show()
            self.start_graphing.setGeometry(10, 340, 316, 30)

            self.mic_type.clear()
            p = pyaudio.PyAudio()
            for inp in range(p.get_device_count()):
                self.mic_type.addItem((p.get_device_info_by_index(inp)['name']))
            self.choise_mic()
        else:
            pass

    def choise_mic(self):
        num_mic = self.mic_type.currentIndex()

    def quit_programm(self):
        sys.exit(1)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())