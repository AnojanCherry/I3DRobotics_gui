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
import time
import cv2
import numpy as np
from PyQt5.QtGui import QIcon, QPixmap, QImage
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
        self.mainWidget = QWidget()
        self.layoutV = QVBoxLayout()
        self.mainWidget.setLayout(self.layoutV)
        self.setCentralWidget(self.mainWidget)

        # Top widgets
        self.top_widget = QWidget()
        self.top_widget.setMaximumHeight(35)
        self.top_widget.setMaximumWidth(60)
        self.StatusIndicator = top_options(self.top_widget)
        self.layoutV.addWidget(self.top_widget)

        # Main widget
        self.mainVideoDispWidget = QWidget()
        self.layoutV.addWidget(self.mainVideoDispWidget)
        self.frameToUpdateImg = QLabel(self.mainVideoDispWidget)

        # Console/Log widget
        #self.console_widget = QWidget()
        #self.layoutV.addWidget(self.console_widget)
        #self.console_widget.setStyleSheet("background-color:red")
        #self.updatedConnectedDeviceList()
    
    def initialiseStereoFrame(self):
        device_class = self.deviceList[self.deviceInd]
        device_info = device_class.device
        camera_name = device_info.getUniqueSerial()
        left_serial = device_info.getLeftCameraSerial()
        right_serial = device_info.getRightCameraSerial()
        device_type = device_class.device_type
        interface_type = phase.stereocamera.CameraInterfaceType.INTERFACE_TYPE_USB

        # setupCalibration files
        left_yaml = cff+"/left.yaml"
        right_yaml = cff+"/right.yaml"

        # Define parameters for read process
        downsample_factor = 1.0
        display_downsample = 0.25
        exposure_value = 10000

        # Check for I3DRSGM license
        stereo_params = phase.stereomatcher.StereoParams(
            phase.stereomatcher.StereoMatcherType.STEREO_MATCHER_I3DRSGM,
            9, 0, 49, False
        )

        # Load calibration
        calibration = phase.calib.StereoCameraCalibration.calibrationFromYAML(
            left_yaml, right_yaml)
        
        # Create stereo matcher
        matcher = phase.stereomatcher.createStereoMatcher(stereo_params)

        # Create stereo camera device information from parameters
        device_info = phase.stereocamera.CameraDeviceInfo(
            left_serial, right_serial, camera_name,
            device_type,
            interface_type)
        # Create stereo camera
        tinaniaCam = phase.stereocamera.TitaniaStereoCamera(device_info)

        # Connect camera and start data capture
        print("Connecting to camera...")
        ret = tinaniaCam.connect()
        if (ret):
            tinaniaCam.startCapture()
            # Set camera exposure value
            tinaniaCam.setExposure(exposure_value)
            print("Running camera capture...")
            while tinaniaCam.isConnected():
                read_result = tinaniaCam.read()
                if read_result.valid:
                    # Rectify stereo image pair
                    rect_image_pair = calibration.rectify(read_result.left, read_result.right)
                    rect_img_left = rect_image_pair.left
                    rect_img_right = rect_image_pair.right

                    match_result = matcher.compute(rect_img_left, rect_img_right)

                    # Check compute is valid
                    if not match_result.valid:
                        print("Failed to compute match")
                        continue

                    # Find the disparity from matcher
                    disparity = match_result.disparity

                    # Convert disparity into 3D pointcloud
                    xyz = phase.disparity2xyz(
                        disparity, calibration.getQ())

                    # Display stereo and disparity images
                    img_left = phase.scaleImage(
                            rect_img_left, display_downsample)
                    img_right = phase.scaleImage(
                            rect_img_right, display_downsample)
                    img_disp = phase.scaleImage(
                            phase.normaliseDisparity(
                                disparity), display_downsample)
                    self.updateVideoFrame(img_disp)
                    '''
#                    cv2.imshow("Left", img_left)
#                    cv2.imshow("Right", img_right)
#                    cv2.imshow("Disparity", img_disp)
#                    c = cv2.waitKey(1)

                    # Save the pointcloud of current frame if 'p' is pressed
                    if c == ord('p'):
                        tme = time.time()
                        out_ply = cff+"/point_cloud"+str(tme)+".ply"
                        save_success = phase.savePLY(out_ply, xyz, rect_img_left)
                        if save_success:
                            print("Pointcloud saved to " + out_ply)
                        else:
                            print("Failed to save pointcloud")
                    
                    # Quit data capture if 'q' is pressed
                    if c == ord('q'):
                        break
                        '''
                else:
                    tinaniaCam.disconnect()
                    raise Exception("Failed to read stereo result")
        return
    
    def updateVideoFrame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.frameToUpdateImg.setPixmap(QPixmap.fromImage(image))
        return

    def updatedConnectedDeviceList(self):
        # Before updating delete all current selected files
        self.menu_connect.clear()
        self.btn_refresh = QAction(QIcon(f"{icon_path}/arrow-circle-double.png"), "Refresh")
        self.btn_refresh.setStatusTip("Click to check for any new Phobos/Titania connected")
        self.btn_refresh.triggered.connect(self.updatedConnectedDeviceList)
        self.menu_connect.addAction(self.btn_refresh)
        self.menu_connect.addSeparator()
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
        self.deviceList.append(Devices(self, device.getUniqueSerial(), device))
        #self.tabLog.update_txt(f"[Event] added {device.getUniqueSerial()}")
        '''
            print("Camera Name: " + device_info.getUniqueSerial())
            print("Left Serial: " + device_info.getLeftCameraSerial())
            print("Right Serial: " + device_info.getRightCameraSerial())
        '''
        return

    def getListNum(self):
        return len(self.deviceList)
    
    def setChosenDevice(self, deviceInd):
        self.deviceInd = deviceInd
        self.StatusIndicator.tlbar_connect.updateStatus(True)
        return

class top_options():
    def __init__(self, parent):
        self.layout = QHBoxLayout()
        parent.setLayout(self.layout)

        # Connect to a device
        self.tlbar_connect = top_option_sub("Calibrate")
        self.tlbar_connect.setPixMap("plug-disconnect-prohibition.png","plug-connect.png")
        self.tlbar_connect.setTip("No device Connected! Connect>Refresh", "Device is bound")
        self.tlbar_connect.updateStatus(False)
        self.layout.addWidget(self.tlbar_connect.lbl)

        # Calibration files
        self.tlbar_cal = top_option_sub("Calibrate")
        self.tlbar_cal.setPixMap("blue-folder--minus.png","blue-folder--plus.png")
        self.tlbar_cal.setTip("Select calibration files")
        self.tlbar_cal.updateStatus(False)
        self.layout.addWidget(self.tlbar_cal.lbl)
        return

class top_option_sub():
    def __init__(self, name):
        self.lbl = QLabel(name)
        self.setPixMap()
        self.setTip()
        self.setAction()
        return
    
    def setPixMap(self, pxmap0=None, pxmap1=None):
        if (pxmap0 == None):
            self.pxmap_path_0 = pxmap0
        else:
            self.pxmap_path_0 = icon_path+"/"+pxmap0

        if (pxmap1 == None):
            self.pxmap_path_1 = pxmap1
        else:
            self.pxmap_path_1 = icon_path+"/"+pxmap1

        return
    
    def setTip(self, tip_0=None, tip_1=None):
        self.tip_0 = tip_0
        self.tip_1 = tip_1
        return
    
    def setAction(self, func_0 = None, func_1 = None):
        self.function_0 = func_0
        self.function_1 = func_1
        return
    
    def updateStatus(self, bol):
        self.bol = bol
        if bol:
            self.lbl.setPixmap(QPixmap(self.pxmap_path_1))
            self.lbl.setToolTip(self.tip_1)
            if (self.function_1 != None):
                self.function_1()
        else:
            self.lbl.setPixmap(QPixmap(self.pxmap_path_0))
            self.lbl.setToolTip(self.tip_0)
            if (self.function_0 != None):
                self.function_0()
        return

class Devices:
    def __init__(self, self_, name, device):
        self.name = name
        self.parent = self_
        self.device = device
        self.device_type = phase.stereocamera.CameraDeviceType.DEVICE_TYPE_TITANIA
        self.id = self_.getListNum()
        btn_connect = QAction("Connect",self_)
        btn_connect.triggered.connect(self.connector)

        #btn_info = QAction("Information",self_)

        sub_menu = self_.menu_connect.addMenu(name)
        sub_menu.addAction(btn_connect)
        #sub_menu.addAction(btn_info)
        return
    
    def connector(self):
        self.selectReferer()
        self.parent.initialiseStereoFrame()
        return
    
    def selectReferer(self):
        self.parent.setChosenDevice(self.id)
        return
    
# Current files folder
cff = os.path.dirname(os.path.realpath(__file__))
icon_path = cff+"/icons"
print(icon_path)

software = QApplication(sys.argv)
mw = mainWindow()
mw.show()
software.exec()