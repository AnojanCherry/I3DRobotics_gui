from py_support.I3DRobotics_gui_draft_10_toolbar import Ui_Form
from PyQt5.QtWidgets import (
    QApplication, QWidget
)

# Inherit from ui2py toolbar file
class toolbar_widgets(Ui_Form):
    def __init__(self, parent):
        super(toolbar_widgets, self).__init__()
        self.parent = parent
        self.setupUi()

        # Connect each button with its intended actions
        self.cbbx_devices.currentIndexChanged.connect(self.event_current_cbbx_device_changed)
        self.btn_devices_connect.clicked.connect(self.event_connectORdisconnect_clicked)
        self.ckbx_Rectify.stateChanged.connect(self.event_rectify_chbx_changed)
        self.ckbx_Stereo.stateChanged.connect(self.event_stereo_chbx_changed)
        self.ckbx_Stereo.setCheckable(False)
        self.ckbx_PointCloud.stateChanged.connect(self.event_point_cloud_chbx_changed)
        self.ckbx_PointCloud.setCheckable(False)
        self.spnbx_exposure.valueChanged.connect(self.event_exposure_changed)
        self.ckbx_capture.toggled.connect(self.event_capture)
        self.ckbx_record.stateChanged.connect(self.event_record)
        return
    
    # Set up recording
    def event_record(self):
        # Set up stream class/object variable to true/false to record constant stream of data
        self.parent.Stream.record_data_bool = self.ckbx_record.isChecked()
        return
    
    # Set up capture so that the image is captured once
    def event_capture(self):
        if self.ckbx_capture.isChecked():
            if (self.parent.capture_data(self.ckbx_capture)):
                self.ckbx_capture.setChecked(False)
                print("Captured successfully")
        return
    
    # Adjust exposure value from the user
    def event_exposure_changed(self):
        self.parent.Stream.changeExposure(self.spnbx_exposure.value())
        return
    
    # Stream on/off point cloud
    def event_point_cloud_chbx_changed(self):
        if not(self.parent.event_child_toolbar_pointCloud_check(self.ckbx_PointCloud.isChecked())):
            self.ckbx_PointCloud.setCheckState(False)
        return
    
    # stream on/off stereo data
    def event_stereo_chbx_changed(self):
        if not(self.parent.event_child_toolbar_stereo_check(self.ckbx_Stereo.isChecked())):
            self.ckbx_PointCloud.setCheckState(False)
            self.ckbx_PointCloud.setCheckable(False)
            self.ckbx_Stereo.setCheckState(False)
        else:
            self.ckbx_PointCloud.setCheckable(True)
        return
    
    # Stream on/off rectified image
    def event_rectify_chbx_changed(self):
        if not(self.parent.event_child_toolbar_rectify_check(self.ckbx_Rectify.isChecked())):
            self.ckbx_PointCloud.setCheckState(False)
            self.ckbx_PointCloud.setCheckable(False)
            self.ckbx_Stereo.setCheckState(False)
            self.ckbx_Stereo.setCheckable(False)
            self.ckbx_Rectify.setCheckState(False)
        else:
            self.ckbx_Stereo.setCheckable(True)
        return
    
    # Connect/disconnect from device
    def event_connectORdisconnect_clicked(self):
        self.parent.ChosenDevice_id = self.cbbx_devices.currentIndex()
        self.parent.event_connectORdisconnect_clicked()
        return
    
    # Setup to run when combobox value changed
    def event_current_cbbx_device_changed(self):
        ind = self.cbbx_devices.currentIndex()
        if (ind>=0):
            self.lbl_device_name.setText(self.parent.device_list[ind].device.getUniqueSerial())
            self.lbl_device_type.setText(self.parent.device_list[ind].name)
        return