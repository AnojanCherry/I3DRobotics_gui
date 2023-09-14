"""!
 @authors Anojan Cherry (anojancherryaji@gmail.com)
 @date 2023-09-14
 @file I3DRobotics_gui_draft_10_toolbar_parent.py
 @brief Simple gui camera to monitor
"""

from py_support.I3DRobotics_gui_draft_10_toolbar import Ui_Form
from PyQt5.QtWidgets import (
    QApplication, QWidget
)

class toolbar_widgets(Ui_Form):
    '''
    The widget that is mounted on top of a Qtoolbar

    Parameter:
        parent (object): The parent class that will create an instance of this class
    
    Inheritance:
        Ui_Form (object): a .ui file to .py file

    Return:
        None
    '''
    def __init__(self, parent):
        super(toolbar_widgets, self).__init__()
        self.parent = parent
        self.setupUi()
        self.cbbx_devices.currentIndexChanged.connect(self.event_current_cbbx_device_changed)
        self.btn_devices_connect.clicked.connect(self.event_connectORdisconnect_clicked)
        self.ckbx_Rectify.stateChanged.connect(self.event_rectify_chbx_changed)
        self.ckbx_Stereo.stateChanged.connect(self.event_stereo_chbx_changed)
        self.ckbx_Stereo.setCheckable(False)
        self.ckbx_PointCloud.stateChanged.connect(self.event_point_cloud_chbx_changed)
        self.ckbx_PointCloud.setCheckable(False)
        self.spnbx_exposure.valueChanged.connect(self.event_exposure_changed)
        self.ckbx_capture.clicked.connect(self.event_capture)
        self.ckbx_record.stateChanged.connect(self.event_record)
        return
    
    def event_record(self):
        '''
        Invoke a function which would refer to the main object, from which it will refer to stream object; From there it will set a variable True/False. The invokation would then save all frames in stream depending on a boolean.

        Parameter:
            None

        Return:
            None
        '''
        self.parent.Stream.record_data_bool = self.ckbx_record.isChecked()
        return
    
    def event_capture(self):
        '''
        Invoke a function which would refer to the main object, from which it will refer to stream object; From there it will set a variable True/False. The invokation would then save all frames in stream depending on a boolean.
        After saving all frames, it would then set itself to False

        Parameter:
            None

        Return:
            None
        '''
        if self.ckbx_capture.isChecked():
            if (self.parent.capture_data(self.ckbx_capture)):
                self.ckbx_capture.setChecked(False)
                print("Captured successfully")
        return
    
    def event_exposure_changed(self):
        '''
        Invoke a function which would refer to the main object, from which it will refer to stream object; From there it will invoke a function which would update the cameras exposure value.

        Parameter:
            None

        Return:
            None
        '''
        self.parent.Stream.changeExposure(self.spnbx_exposure.value())
        return
    
    def event_point_cloud_chbx_changed(self):
        '''
        Invoke a function from main object which will inform the stream to either start/stop point cloud.

        Parameter:
            None

        Return:
            None
        '''
        if not(self.parent.event_child_toolbar_pointCloud_check(self.ckbx_PointCloud.isChecked())):
            self.ckbx_PointCloud.setCheckState(False)
        return
    
    def event_stereo_chbx_changed(self):
        '''
        Invoke a function from main object which will inform the stream to either start/stop stereo.

        Parameter:
            None

        Return:
            None
        '''
        if not(self.parent.event_child_toolbar_stereo_check(self.ckbx_Stereo.isChecked())):
            self.ckbx_PointCloud.setCheckState(False)
            self.ckbx_PointCloud.setCheckable(False)
            self.ckbx_Stereo.setCheckState(False)
        else:
            self.ckbx_PointCloud.setCheckable(True)
        return
    
    def event_rectify_chbx_changed(self):
        '''
        Invoke a function from main object which will inform the stream to either rectify/unrectify.

        Parameter:
            None

        Return:
            None
        '''
        if not(self.parent.event_child_toolbar_rectify_check(self.ckbx_Rectify.isChecked())):
            self.ckbx_PointCloud.setCheckState(False)
            self.ckbx_PointCloud.setCheckable(False)
            self.ckbx_Stereo.setCheckState(False)
            self.ckbx_Stereo.setCheckable(False)
            self.ckbx_Rectify.setCheckState(False)
        else:
            self.ckbx_Stereo.setCheckable(True)
        return
    
    def event_connectORdisconnect_clicked(self):
        '''
        Invoke a function from main object which will inform the stream to connect/disconnect and start/stop stream from a camera.

        Parameter:
            None

        Return:
            None
        '''
        self.parent.ChosenDevice_id = self.cbbx_devices.currentIndex()
        self.parent.event_connectORdisconnect_clicked()
        return
    
    def event_current_cbbx_device_changed(self):
        '''
        Invoke a function that updates the labels in toolbar gui, that everytime a new device is selected in the dropdown box.

        Parameter:
            None

        Return:
            None
        '''
        ind = self.cbbx_devices.currentIndex()
        if (ind>=0):
            self.lbl_device_name.setText(self.parent.device_list[ind].device.getUniqueSerial())
            self.lbl_device_type.setText(self.parent.device_list[ind].name)
        return
