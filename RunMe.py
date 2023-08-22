from py_support.I3DRobotics_gui_draft_10_mainDisp_parent import mainDisp
from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = mainDisp()
    ui.show()
    sys.exit(app.exec_())