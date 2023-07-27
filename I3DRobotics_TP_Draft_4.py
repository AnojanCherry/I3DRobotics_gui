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
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget,
    QAction, QSplitter, QTabWidget, QFrame,
    QLabel, QToolBar,QTreeWidget, QScrollArea
)

import phase.pyphase as phase

class mainWindow(QMainWindow):
    def __init__(self, title="I3DRobotics"):
        super(mainWindow, self).__init__()

        self.deviceList = []

        self.setWindowTitle(title)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.mainMenu = self.menuBar()
        
        self.btn_refresh = QAction(QIcon(f"{icon_path}/arrow-circle-double.png"), "Refresh", self)
        self.btn_refresh.setStatusTip("Click to check for any new Phobos/Titania connected")
        self.btn_refresh.triggered.connect(self.updatedConnectedDeviceList)
        
        self.menu_connect = self.mainMenu.addMenu("Connect")
        self.menu_connect.addAction(self.btn_refresh)
        self.menu_connect.addSeparator()

        self.btn_stereo = QAction("Stereo", self)
        self.btn_stereo.setStatusTip("Check stereo image")
        #self.btn_stereo.setCheckable(True)
        self.mainMenu.addAction(self.btn_stereo)

        self.btn_pointCloud = QAction("Point cloud", self)
        self.btn_pointCloud.setStatusTip("Check stereo image")
        #self.btn_pointCloud.setCheckable(True)
        self.mainMenu.addAction(self.btn_pointCloud)   

        self.btn_preferences = QAction("Preferences", self)
        self.mainMenu.addAction(self.btn_preferences)

        self.tab_disp_split = QSplitter()

        self.mainDispFrame = QFrame()
        self.widgetFrame = QFrame()
        self.widgetExpansionFrame = QFrame()

        #self.tab_disp_split.addWidget(self.msgConsole)
        self.tab_disp_split.addWidget(self.widgetFrame)
        self.tab_disp_split.addWidget(self.widgetExpansionFrame)
        self.tab_disp_split.addWidget(self.mainDispFrame)

        self.msgConsole = QTabWidget()
        self.tabProblems = consolelog()
        self.tabProblems.initGui("[System] System initiated...")
        self.tabLog = consolelog()
        self.tabLog.initGui("[System] System initiated...")
        self.msgConsole.addTab(self.tabProblems, "Problems")
        self.msgConsole.addTab(self.tabLog, "Log")

        self.toolbar = QToolBar(self)
        self.toolbar.addWidget(self.msgConsole)
        self.toolbar.setMinimumHeight(100)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbar)

        self.setCentralWidget(self.tab_disp_split)
        self.updatedConnectedDeviceList()
    
    def updatedConnectedDeviceList(self):
        self.tabLog.update_txt("[Event] Refreshing device list")
        #self.tabProblems.update_txt("[TBDL] Update connected device list")
        #self.updateIndividualDeviceList("Phobos")
        for i in self.deviceList:
            del i
        device_infos = phase.stereocamera.availableDevices()
        if len(device_infos) <=0 :
            self.tabLog.update_txt("[System] No device found")
            #self.menu_connect
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
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        return
    
class consolelog(QScrollArea):
    def _init__(self, txt=None):
        super().__init__()
        self.initGui()
        return
    
    def initGui(self, msg = None):
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.lbl = QLabel()
        self.setWidget(self.lbl)
        self.txt = []
        self.maxLine = 50
        if msg != None:
            self.update_txt(msg)
        return
    
    def update_txt(self, txt):
        if len(self.txt)>= self.maxLine:
            del self.txt[0]
        self.txt.append(txt)
        str = ""
        for i in self.txt:
            str+=i+"\n"
        self.lbl.setText(str)
        return

# Current files folder
cff = os.path.dirname(os.path.realpath(__file__))
icon_path = cff+"/icons"
print(icon_path)

software = QApplication(sys.argv)
mw = mainWindow()
mw.show()
software.exec()