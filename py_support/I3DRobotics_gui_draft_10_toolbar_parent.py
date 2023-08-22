from py_support.I3DRobotics_gui_draft_10_toolbar import Ui_Form
from PyQt5.QtWidgets import (
    QApplication, QWidget
)

class toolbar_widgets(Ui_Form):
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
        #self.slider_downSample.valueChanged.connect(self.event_downsampleValueChanged)
        #self.spnbx_downSample_factor.valueChanged.connect(self.event_downsampleFactorValueChanged)
        self.ckbx_capture.toggled.connect(self.event_capture)
        self.ckbx_record.stateChanged.connect(self.event_record)
        return
    
    def event_record(self):
        self.parent.Stream.record_data_bool = self.ckbx_record.isChecked()
        return
    
    def event_capture(self):
        if self.ckbx_capture.isChecked():
            if (self.parent.capture_data(self.ckbx_capture)):
                self.ckbx_capture.setChecked(False)
                print("Captured successfully")
        return
    
    #def event_downsampleFactorValueChanged(self):
    #    print(self.spnbx_downSample_factor.value())
    #    self.lbl_downSample_factor_value = self.spnbx_downSample_factor.value()
    #    self.parent.Stream.downsample_factor = self.spnbx_downSample_factor.value()
    #    return
    
    #def event_downsampleValueChanged(self):
    #    print(self.slider_downSample.value())
    #    self.lbl_downSample_value = self.slider_downSample.value()
    #    self.parent.Stream.display_downsample = self.slider_downSample.value()
    #    return
    
    def event_exposure_changed(self):
        self.parent.Stream.changeExposure(self.spnbx_exposure.value())
        return
    
    def event_point_cloud_chbx_changed(self):
        if not(self.parent.event_child_toolbar_pointCloud_check(self.ckbx_PointCloud.isChecked())):
            self.ckbx_PointCloud.setCheckState(False)
        return
    
    def event_stereo_chbx_changed(self):
        if not(self.parent.event_child_toolbar_stereo_check(self.ckbx_Stereo.isChecked())):
            self.ckbx_PointCloud.setCheckState(False)
            self.ckbx_PointCloud.setCheckable(False)
            self.ckbx_Stereo.setCheckState(False)
        else:
            self.ckbx_PointCloud.setCheckable(True)
        return
    
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
    
    def event_connectORdisconnect_clicked(self):
        self.parent.ChosenDevice_id = self.cbbx_devices.currentIndex()
        self.parent.event_connectORdisconnect_clicked()
        return
    
    def event_current_cbbx_device_changed(self):
        ind = self.cbbx_devices.currentIndex()
        if (ind>=0):
            self.lbl_device_name.setText(self.parent.device_list[ind].device.getUniqueSerial())
            self.lbl_device_type.setText(self.parent.device_list[ind].name)
        return