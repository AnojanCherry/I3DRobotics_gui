from PyQt5 import QtGui
from py_support.I3DRobotics_gui_draft_10_mainDisp import Ui_mainWindow
from py_support.I3DRobotics_gui_draft_10_toolbar_parent import toolbar_widgets
from py_support.I3DRobotics_gui_draft_10_StreamService_2 import Stream
from py_support.I3DRobotics_gui_draft_10_devices import Devices

from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import (
    QToolBar, QMainWindow, QAction
)

import phase.pyphase as phase

import time, os

class mainDisp(Ui_mainWindow):
    # Chosen Device class
    ChosenDevice = False
    ChosenDevice_id = False
    device_list = []

    # When the window is resized, resize the frames aswell
    def resizeEvent(self, a0):
        try:
            self.Stream.WindowresizeEvent()
        except Exception as e:
            print(str(e))
        return super().resizeEvent(a0)

    def __init__(self):
        super(mainDisp, self).__init__()
        # This class inherits from ui_mainwindow class line 16
        self.setupUi()

        # Everything inside toolbar are in child class "toolbar_widgets"
        self.toolbar = QToolBar("Tools")
        self.toolbar_main = toolbar_widgets(self)
        self.toolbar_main.btn_devices_refresh.clicked.connect(self.event_refresh_clicked)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.toolbar.addWidget(self.toolbar_main.gridLayoutWidget)

        self.Stream = Stream(self.mainDisplay, self)
        self.Stream.start()

        self.event_refresh_clicked()
        return
    
    def event_child_toolbar_rectify_check(self, SetAsTrue):
        if (self.ChosenDevice==False):
            return False
        elif not(os.path.isfile(self.ChosenDevice.left_yaml)):
            return False
        elif not(os.path.isfile(self.ChosenDevice.right_yaml)):
            return False
        if SetAsTrue:
            self.Stream.setup_rectifier(self.ChosenDevice.left_yaml,self.ChosenDevice.right_yaml)
            return True
        else:
            self.Stream.setup_raw()
            return False
        
    def event_child_toolbar_stereo_check(self, SetAsTrue):
        if (self.ChosenDevice==False):
            return False
        if SetAsTrue:
            self.Stream.setup_stereo()
            return True
        else:
            self.event_child_toolbar_rectify_check(True)
            return False
        
    def event_child_toolbar_pointCloud_check(self, SetAsTrue):
        if (self.ChosenDevice==False):
            return False
        if SetAsTrue:
            self.Stream.setup_pointCloud()
            return True
        else:
            self.event_child_toolbar_stereo_check(True)
            return False
        
    def capture_data(self, capturebool):
        if capturebool:
            return self.Stream.capture_data(capturebool)
    
    # Function to execute for when refreshing for devices
    def event_refresh_clicked(self):
        self.device_list.clear()
        self.toolbar_main.cbbx_devices.clear()

        # Update Menu
        self.menuDevice.clear()
        self.actionRefresh = QAction(self)
        self.actionRefresh.setObjectName("actionRefresh")
        self.menuDevice.addAction(self.actionRefresh)
        self.actionRefresh.triggered.connect(self.event_refresh_clicked)
        self.menuDevice.addSeparator()
        self.actionRefresh.setText("Refresh")

        # Get all connected cams
        device_infos = phase.stereocamera.availableDevices()
        if (str(self.ChosenDevice_id) != str(False)):
            self.device_list.append(self.ChosenDevice)
            self.ChosenDevice_id = 0
            self.device_list[0].id = 0
            self.toolbar_main.cbbx_devices.addItem(f"{self.ChosenDevice.id+1}. {self.ChosenDevice.name}")
        if (len(device_infos) <=0) :
            if (str(self.ChosenDevice_id) == str(False)):
                print("[TBDL] No device found!")
        else:
            for device in device_infos:
                device_i = Devices(self, device, len(self.device_list))
                self.device_list.append(device_i)
                self.toolbar_main.cbbx_devices.addItem(f"{device_i.id+1}. {device_i.name}")
        return
    
    # Connect to chosen Device
    def event_connectORdisconnect_clicked(self):
        print("Attempting connect/Disconnect")
        if (str(self.ChosenDevice_id) != "False"):
            self.ChosenDevice = self.device_list[self.ChosenDevice_id]
        elif (str(self.ChosenDevice_id) == "False"):
            print("Error! no device specified")
            
        if str(self.ChosenDevice_id) != str(False):
            if (self.Stream.pause == False):
                print("Closing connection")
                self.ChosenDevice.btn_connect.setText("Connect")
                self.toolbar_main.btn_devices_connect.setText("Connect")
                self.ChosenDevice_id = False
                self.ChosenDevice = False
                self.Stream.pause = True
                time.sleep(2)
            else:
                print("Establishing connection")
                self.ChosenDevice.btn_connect.setText("Disconnect")
                self.toolbar_main.btn_devices_connect.setText("Disconnect")
                self.Stream.update_Device(self.ChosenDevice)
                self.Stream.pause = False
                time.sleep(2)
        return