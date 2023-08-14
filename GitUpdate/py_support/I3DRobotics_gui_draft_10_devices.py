from PyQt5.QtWidgets import (
    QAction
)

import phase.pyphase as phase 

import os

class Devices():
    def __init__(self, parent, device, id):
        self.parent = parent
        self.device = device
        self.id = id

        if "70686f626f" in str(device.getUniqueSerial()):
            self.name = "Phobos"
            self.device_type = phase.stereocamera.CameraDeviceType.DEVICE_TYPE_PHOBOS
        elif "746974616" in str(device.getUniqueSerial()):
            self.name = "Titania"
            self.device_type = phase.stereocamera.CameraDeviceType.DEVICE_TYPE_TITANIA
        else:
            self.name = device.getUniqueSerial()
        
        self.btn_connect = QAction("Connect",parent)
        self.btn_connect.triggered.connect(self.event_connectORdisconnect_clicked)
        device_menu = parent.menuDevice.addMenu(self.name)
        device_menu.addAction(self.btn_connect)
        cwf = os.path.dirname(os.path.realpath(__file__)) #Current working folder
        self.left_yaml = os.path.join(cwf,"left.yaml")
        self.right_yaml = os.path.join(cwf,"right.yaml")
        print(self.left_yaml)
        return
    
    def event_connectORdisconnect_clicked(self):
        print("Device", (self.parent.ChosenDevice_id))
        if ((self.btn_connect.text() == "Connect") and (str(self.parent.ChosenDevice_id) == str(False))):
            print("device connect")
            self.parent.ChosenDevice_id = self.id
            self.parent.event_connectORdisconnect_clicked()
        elif ((self.btn_connect.text() == "Connect") and (str(self.parent.ChosenDevice_id) != str(False))):
            print("device Disconnect")
            self.parent.event_connectORdisconnect_clicked()
            self.parent.ChosenDevice_id = self.id
            print("device connect")
            self.parent.event_connectORdisconnect_clicked()
        elif(self.btn_connect.text() == "Disconnect"):
            print("device connect")
            self.parent.event_connectORdisconnect_clicked()
            return
        return