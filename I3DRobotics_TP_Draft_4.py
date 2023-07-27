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

        # main window
        self.setWindowTitle(title)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)


        # Menu bar
        self.mainMenu = self.menuBar()
            
            # Sub menu - connect
        self.menu_connect = self.mainMenu.addMenu("Connect")
        
                # Sub menu - connect - Refresh item 1
        self.btn_refresh = QAction(QIcon(f"{icon_path}/arrow-circle-double.png"), "Refresh", self)
        self.btn_refresh.setStatusTip("Click to check for any new Phobos/Titania connected")
        self.btn_refresh.triggered.connect(self.updatedConnectedDeviceList)
        self.menu_connect.addAction(self.btn_refresh)
        self.menu_connect.addSeparator()
        
            # Sub menu - Stereo
        self.btn_stereo = QAction("Stereo", self)
        self.btn_stereo.setStatusTip("Check stereo image")
        self.mainMenu.addAction(self.btn_stereo)

            # Sub menu - Point cloud
        self.btn_pointCloud = QAction("Point cloud", self)
        self.btn_pointCloud.setStatusTip("Check stereo image")
        self.mainMenu.addAction(self.btn_pointCloud)   

            # Sub menu - Preferences
        self.btn_preferences = QAction("Preferences", self)
        self.mainMenu.addAction(self.btn_preferences)


        # Bottom console
        self.msgConsole = QTabWidget()

            # Bottom console - log data
        self.tabLog = consolelog()
        self.tabLog.subInit("[System] System initiated...")
        self.msgConsole.addTab(self.tabLog, "Log")

            # Bottom console - problems data
        self.tabProblems = consolelog()
        self.tabProblems.subInit("[System] System initiated...")
        self.msgConsole.addTab(self.tabProblems, "Problems")

            # Bottom toolbar - compile
        self.toolbar = QToolBar(self)
        self.toolbar.addWidget(self.msgConsole)
        self.toolbar.setMinimumHeight(100)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbar)

        
        # Main window
        self.tab_disp_split = QSplitter()

            # Sub widget frame
        self.widgetFrame = QWidget()
        btn = QAction("btun", self)
        self.widgetFrame.addAction(self.btn_pointCloud)
        self.widgetFrame.setStyleSheet("background-color: red")
        lbl = QLabel()
        lbl.setText("Hello world")
        self.tab_disp_split.addWidget(self.widgetFrame)

            # Sub widget expantion frame
        self.widgetExpansionFrame = QFrame()
        self.tab_disp_split.addWidget(self.widgetExpansionFrame)

            # Sub main display frame
        self.mainDispFrame = QFrame()
        self.tab_disp_split.addWidget(self.mainDispFrame)

        self.setCentralWidget(self.tab_disp_split)
        self.updatedConnectedDeviceList()
    
    def updatedConnectedDeviceList(self):
        for i in self.deviceList:
            del i
        device_infos = phase.stereocamera.availableDevices()
        if len(device_infos) <=0 :
            self.tabLog.update_txt("[System] No device found")
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
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        return
    
class subWidgetFrame(QFrame):
    def __init__(self):
        super().__init__()
        return
    
    def subInit(self, self_):
        self.btn_file = QAction("Files", self_)
        self.addAction(self.btn_file)
        return
    

    
class consolelog(QScrollArea):
    def _init__(self, txt=None):
        super().__init__()
        return
    
    def subInit(self, msg = None):
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