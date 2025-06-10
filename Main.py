import sys
import pyaudio


from PyQt5 import (
    QtCore,
    QtGui,
    QtWidgets,
    uic
)
from PyQt5.QtWidgets import *


class Main(QMainWindow):
    def __init__(self):
        """
        Initialized frontend.
        """
        super(Main, self).__init__()
        uic.loadUi('mainUI.ui', self)

        # Visual temporary settings.
        self.input_type.setEditable(True)
        self.input_type.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.input_type.lineEdit().setFont(QtGui.QFont('Roboto Slab', 12))
        self.input_type.lineEdit()
        self.input_type.lineEdit().setReadOnly(True)

        # Connect interfaces with functions.
        self.path.clicked.connect(self.get_path)
        self.input_type.currentIndexChanged.connect(self.choise_changed)
        self.rec_type.currentIndexChanged.connect(self.choise_recording)
        self.model_type.currentIndexChanged.connect(self.choise_model)

        #Hiding elements.
        self.line_5.hide()
        self.line_6.hide()
        self.line_7.hide()
        self.line_8.hide()
        self.path.hide()
        self.path_sound_text.hide()
        self.path_text.hide()
        self.rec_type_text.hide()
        self.rec_type.hide()
        self.start_sound.hide()
        self.stop_sound.hide()

    def get_path(self):
        """
        Getting file path.
        """
        path = QtWidgets.QFileDialog.getOpenFileName()
        self.path_sound_text.setText(path[0])

    def choise_changed(self):
        """
        Change visual.
        """
        if self.input_type.currentText() == 'Аудиомодель':
            self.A_reg.show()
            self.A_reg_text.show()
            self.f_reg.show()
            self.f_reg_text.show()
            self.fi_reg.show()
            self.fi_reg_text.show()
            self.line_5.hide()
            self.line_6.hide()
            self.line_7.hide()
            self.line_8.hide()
            self.model_type.show()
            self.omega_reg.show()
            self.omega_reg_text.show()
            self.path.hide()
            self.path_sound_text.hide()
            self.path_text.hide()
            self.rec_type_text.hide()
            self.rec_type.hide()
            self.start_sound.hide()
            self.stop_sound.hide()
            self.t_reg.show()
            self.t_reg_text.show()
        elif self.input_type.currentText() == 'Файл':
            self.A_reg.hide()
            self.A_reg_text.hide()
            self.f_reg.hide()
            self.f_reg_text.hide()
            self.fi_reg.hide()
            self.fi_reg_text.hide()
            self.line_5.show()
            self.line_6.hide()
            self.line_7.hide()
            self.line_8.hide()
            self.model_type.hide()
            self.omega_reg.hide()
            self.omega_reg_text.hide()
            self.path.show()
            self.path_sound_text.show()
            self.path_text.show()
            self.rec_type_text.hide()
            self.rec_type.hide()
            self.start_graphing.setGeometry(10, 300, 316, 30)
            self.start_sound.hide()
            self.stop_sound.hide()
            self.t_reg.hide()
            self.t_reg_text.hide()
        elif self.input_type.currentText() == 'Звуки устройства':
            self.A_reg.hide()
            self.A_reg_text.hide()
            self.f_reg.hide()
            self.f_reg_text.hide()
            self.fi_reg.hide()
            self.fi_reg_text.hide()
            self.line_5.hide()
            self.line_6.show()
            self.line_7.show()
            self.line_8.show()
            self.model_type.hide()
            self.omega_reg.hide()
            self.omega_reg_text.hide()
            self.path.hide()
            self.path_sound_text.hide()
            self.path_text.hide()
            self.rec_type_text.show()
            self.rec_type.show()
            self.rec_type.clear()
            self.start_graphing.setGeometry(10, 340, 316, 30)
            self.start_sound.show()
            self.stop_sound.show()
            self.t_reg.hide()
            self.t_reg_text.hide()

            pya = pyaudio.PyAudio()
            for inpt in range(pya.get_device_count()):
                self.rec_type.addItem((pya.get_device_info_by_index(inpt)['name']))
            self.choise_recording()
        else:
            pass

    def choise_model(self):
        """
        Visualising params
        """
        if self.model_type.currentIndex() == 'a(t) = Acos(ωt + φ)':
            self.A_reg.show()
            self.A_reg_text.show()
            self.f_reg.hide()
            self.f_reg_text.hide()
            self.fi_reg.hide()
            self.fi_reg_text.hide()
            self.omega_reg.show()
            self.omega_reg_text.show()
            self.t_reg.show()
            self.t_reg_text.show()
        else:
            pass

    def choise_recording(self):
        """
        Getting method of record.
        """
        num_mic = self.rec_type.currentIndex()

    def quit_program(self):
        """
        Exit program.
        """
        sys.exit(1)


def except_hook(cls, exception, traceback):
    """
    Get error and exception.
    """
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())