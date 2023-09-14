"""!
 @authors Anojan Cherry (anojancherryaji@gmail.com)
 @date 2023-09-14
 @file I3DRobotics_gui_draft_10_mainDisp_parent.py
 @brief Simple gui camera to monitor
"""

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
    '''
    Main container that will connect all other scripts

    Parameter:
        None
    
    Inheritance:
        Ui_mainWindow (object): a .ui file to .py file
    
    Return:
        None
    '''

    # 
    ChosenDevice = False
    ChosenDevice_id = False
    device_list = []

    def resizeEvent(self, a0):
        '''
        When the main gui is resized, resize the image frame

        Parameter:
            a0: resize parameters that the system pass itself when resizing.

        Return:
            None
        '''
        try:
            self.Stream.WindowresizeEvent()
        except Exception as e:
            print(str(e))
        return super().resizeEvent(a0)

    def __init__(self):
        '''
        Initiate the main gui

        Parameter:
            None
        
        Return:
            None
        '''
        super(mainDisp, self).__init__()
        self.setupUi()

        # Toolbar section
        self.toolbar = QToolBar("Tools")
        self.toolbar_main = toolbar_widgets(self)
        self.toolbar_main.btn_devices_refresh.clicked.connect(self.event_refresh_clicked)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        self.toolbar.addWidget(self.toolbar_main.gridLayoutWidget)

        # Anything and everything that happens in the thread are in here
        self.Stream = Stream(self.mainDisplay, self)
        self.Stream.start()

        self.event_refresh_clicked()
        return
    
    def event_child_toolbar_rectify_check(self, SetAsTrue: bool):
        '''
        When the user tick/untick rectify, Check if there are any yaml files and a device is connected ,then request the thread to rectify/unrectify.

        Parameter:
            SetAsTrue (bool):   True - to rectify. False - to n rectify
        
        Return:
            bool - True if rectified, False if unrectified
        '''
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
        
    def event_child_toolbar_stereo_check(self, SetAsTrue: bool):
        '''
        When the user tick/untick, Check if a device is connected ,then request the thread to start/stop stereo streaming. if the process fails return false, else return true.

        Parameter:
            SetAsTrue (bool):   True - to start streaming stereo, False - to stop streaming stereo
        
        Return:
            bool - True if stereo started streaming, False if stereo stopped streaming
        '''
        if (self.ChosenDevice==False):
            return False
        if SetAsTrue:
            self.Stream.setup_stereo()
            return True
        else:
            self.event_child_toolbar_rectify_check(True)
            return False
        
    def event_child_toolbar_pointCloud_check(self, SetAsTrue):
        '''
        When the user tick/untick, Check if a device is connected ,then request the thread to start/stop point cloud streaming. if the process fails return false, else return true.

        Parameter:
            SetAsTrue (bool):   True - to start streaming point cloud, False - to stop streaming point cloud
        
        Return:
            bool - True if point cloud started streaming, False if point cloud stopped streaming
        '''
        if (self.ChosenDevice==False):
            return False
        if SetAsTrue:
            self.Stream.setup_pointCloud()
            return True
        else:
            self.event_child_toolbar_stereo_check(True)
            return False
        
    def capture_data(self):
        return self.Stream.capture_data()
    
    # Function to execute for when refreshing for devices
    def event_refresh_clicked(self):
        '''
        This function would check for currently connected device and update it to the dropdown box

        Parameter:
            None
        
        Return:
            None
        '''
        # Clear the currently connected device list
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
            #  self.device_list[0].id = 0
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
        '''
        When connect/disconnect is pressed, this would then connect/disconnect from the device.

        Parameter:
            none

        Return:
            None
        '''
        print("Attempting connect/Disconnect")
        if (str(self.ChosenDevice_id) != "False" and (self.ChosenDevice_id>=0)):
            self.ChosenDevice = self.device_list[self.ChosenDevice_id]
        elif (str(self.ChosenDevice_id) == "False"):
            print("Error! no device specified")
        elif not(self.ChosenDevice_id>=0):
            print("Error! no device chosen")
            
        if str(self.ChosenDevice_id) != str(False) and (self.ChosenDevice_id>=0):
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
        else:
            print()
        return
