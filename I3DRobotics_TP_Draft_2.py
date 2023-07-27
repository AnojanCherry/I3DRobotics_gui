#!/usr/bin/env python3
'''

    @Author Anojan Raveendran
    @email  anojan.raveendran@city.ac.uk
    @brief  A software to test out my skills

    References:
        https://www.pythonguis.com/tutorials/pyqt-actions-toolbars-menus/
        https://p.yusukekamiyamane.com/

'''

# Imports
import sys
import typing
import os
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QAction
)

class mainWindow(QMainWindow):
    def __init__(self, title="I3DRobotics"):
        super(mainWindow, self).__init__()

        self.deviceList = []

        self.setWindowTitle(title)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        mainMenu = self.menuBar()
        
        btn_refresh = QAction(QIcon(f"{icon_path}/arrow-circle-double.png"), "Refresh", self)
        btn_refresh.setStatusTip("Click to check for any new Phobos/Titania connected")
        btn_refresh.triggered.connect(self.updatedConnectedDeviceList)
        
        self.menu_connect = mainMenu.addMenu("Connect")
        self.menu_connect.addAction(btn_refresh)

        btn_stero = QAction("Stereo", self)
        btn_stero.setStatusTip("Check stereo image")
        #btn_stero.setCheckable(True)
        mainMenu.addAction(btn_stero)

        btn_pointcloud = QAction("Point cloud", self)
        btn_pointcloud.setStatusTip("Check stereo image")
        #btn_pointcloud.setCheckable(True)
        mainMenu.addAction(btn_pointcloud)   

        self.updatedConnectedDeviceList()     
    
    def updatedConnectedDeviceList(self):
        print("[Event] Refreshing device list")
        print("[TBDL] Update connected device list")
        self.updateIndividualDeviceList("Phobos")
        self.updateIndividualDeviceList("Titania")
        return
    
    def updateIndividualDeviceList(self, name):
        if len(self.deviceList) == 0:
            self.menu_connect.addSeparator()
        self.deviceList.append(Devices(self, name))
        print(f"[Event] added {name}")
        return
    
class Devices:
    def __init__(self, self_, name):
        self.name = name
        btn_connect = QAction("Connect",self_)

        btn_info = QAction("Information",self_)

        sub_menu = self_.menu_connect.addMenu(name)
        sub_menu.addAction(btn_connect)
        sub_menu.addAction(btn_info)
        return
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        return

# Current files folder
cff = os.path.dirname(os.path.realpath(__file__))
icon_path = cff+"/icons"
print(icon_path)

software = QApplication(sys.argv)
mw = mainWindow()
mw.show()
software.exec()