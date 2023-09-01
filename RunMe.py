'''

    @Author Anojan Raveendran
    @email  anojan.raveendran@city.ac.uk
    @brief  A simple gui to display data from camera

    References:
        https://www.pythonguis.com/tutorials/pyqt-actions-toolbars-menus/
        https://p.yusukekamiyamane.com/

'''

from py_support.I3DRobotics_gui_draft_10_mainDisp_parent import mainDisp
from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Creates a main disp object
    ui = mainDisp()
    ui.show()
    sys.exit(app.exec_())