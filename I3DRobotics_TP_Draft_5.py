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
from PyQt5 import QtCore
import sys
import typing
import os
import datetime
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QAction, QSplitter, QTabWidget, QFrame,
    QLabel, QToolBar,QTreeWidget, QScrollArea,
    QVBoxLayout, QHBoxLayout
)

import phase.pyphase as phase

class mainWindow(QMainWindow):
    def __init__(self, title="I3DRobotics"):
        super(mainWindow, self).__init__()

        self.deviceList = []

        # main window
        self.setWindowTitle(title)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)


        # Menu bar
        self.mainMenu = self.menuBar()
            
            # Sub menu - connect
        self.menu_connect = self.mainMenu.addMenu("Connect")
        
                # Sub menu - connect - Refresh item 1
        self.btn_refresh = QAction(QIcon(f"{icon_path}/arrow-circle-double.png"), "Refresh")
        self.btn_refresh.setStatusTip("Click to check for any new Phobos/Titania connected")
        self.btn_refresh.triggered.connect(self.updatedConnectedDeviceList)
        self.menu_connect.addAction(self.btn_refresh)
        self.menu_connect.addSeparator()
        
            # Sub menu - Stereo
        self.btn_stereo = QAction("Stereo")
        self.btn_stereo.setStatusTip("Check stereo image")
        self.mainMenu.addAction(self.btn_stereo)

            # Sub menu - Point cloud
        self.btn_pointCloud = QAction("Point cloud")
        self.btn_pointCloud.setStatusTip("Check stereo image")
        self.mainMenu.addAction(self.btn_pointCloud)   

            # Sub menu - Preferences
        self.btn_preferences = QAction("Preferences")
        self.mainMenu.addAction(self.btn_preferences)

        
        # Main window
        self.mainDisp = mainDisp()

        self.setCentralWidget(self.mainDisp.mainWidget)
        #self.updatedConnectedDeviceList()

    def updatedConnectedDeviceList(self):
        # Before updating delete all current selected files
        for i in self.deviceList:
            del i

        # Get all connected cams
        device_infos = phase.stereocamera.availableDevices()
        if not(len(device_infos) <=0) :
            #self.tabLog.update_txt("[System] No device found")
            print("[TBDL] No device found!")
            for i in self.deviceList:
                del i
        else:
            for device in device_infos:
                self.updateIndividualDeviceList(device)
        return
    
    def updateIndividualDeviceList(self, device):
        self.deviceList.append(device)
        self.tabLog.update_txt(f"[Event] added {device.getUniqueSerial()}")
        '''
            print("Camera Name: " + device_info.getUniqueSerial())
            print("Left Serial: " + device_info.getLeftCameraSerial())
            print("Right Serial: " + device_info.getRightCameraSerial())
        '''
        return

class mainDisp():
    def __init__(self):
        self.mainWidget = QWidget()
        self.layoutV = QVBoxLayout()
        self.mainWidget.setLayout(self.layoutV)

        # Top widgets
        self.top_widget = QWidget()
        self.top_widget.setMaximumHeight(20)
        self.layoutHSpliter = top_options(self.top_widget)
        self.layoutHSpliter.main.setOrientation(Qt.Horizontal)
        self.layoutV.addWidget(self.top_widget)

        # Main widget
        self.mainDispWidget = mainDispStereo()
        self.layoutV.addWidget(self.mainDispWidget.mainWidget)

        # Console/Log widget
        #self.console_widget = QWidget()
        #self.layoutV.addWidget(self.console_widget)
        #self.console_widget.setStyleSheet("background-color:red")
        return

class top_options():
    def __init__(self, parent):
        self.main = QSplitter(parent)

        # Connect to a device
        self.tlbar_connect = top_option_sub("Calibrate")
        self.tlbar_connect.setPixMap("plug-disconnect-prohibition.png","plug-connect.png")
        self.tlbar_connect.setTip("No device Connected! Connect>Refresh")
        self.tlbar_connect.changeImg(False)
        self.main.addWidget(self.tlbar_connect.lbl)

        # Calibration files
        self.tlbar_cal = top_option_sub("Calibrate")
        self.tlbar_cal.setPixMap("blue-folder--minus.png","blue-folder--plus.png")
        self.tlbar_cal.setTip("Select calibration files")
        self.tlbar_cal.changeImg(False)
        self.main.addWidget(self.tlbar_cal.lbl)
        return

class top_option_sub():
    def __init__(self, name):
        self.lbl = QLabel(name)
        return
    
    def setPixMap(self, pxmap0, pxmap1):
        self.pxmap_path_0 = icon_path+"/"+pxmap0
        self.pxmap_path_1 = icon_path+"/"+pxmap1
        return
    
    def setTip(self, tip_0=None, tip_1=None):
        self.tip_0 = tip_0
        self.tip_1 = tip_1
        return
    
    def setAction(self, function):
        return
    
    def changeImg(self, bol):
        self.bol = bol
        if bol:
            self.lbl.setPixmap(QPixmap(self.pxmap_path_1))
            if (self.tip_1 != None):
                self.lbl.setToolTip(self.tip_1)
        else:
            self.lbl.setPixmap(QPixmap(self.pxmap_path_0))
            if (self.tip_0 != None):
                self.lbl.setToolTip(self.tip_0)
        return
    
class mainDispStereo():
    def __init__(self):
        self.mainWidget = QWidget()
        return

# Current files folder
cff = os.path.dirname(os.path.realpath(__file__))
icon_path = cff+"/icons"
print(icon_path)

software = QApplication(sys.argv)
mw = mainWindow()
mw.show()
software.exec()