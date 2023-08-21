from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, QThread

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel
)

import phase.pyphase as phase

import time, cv2, os, random

import numpy as np
import open3d as o3d
#import matplotlib.pyplot as plt

class Stream(QThread):

    # Define parameters for read process
    downsample_factor = 1.0
    display_downsample = 0.25
    exposure_value = 10000

    pcSimStarted = False
    vis = False

    record_data_bool = False

    for dirpath, dirnames, filenames in os.walk("."):
        if "misc" in dirpath:
            pcDataFolder = dirpath
    
    def file_exists(self, file_to_check):
        for dirpath, dirnames, filenames in os.walk("."):
                for filename in [f for f in filenames if (f.endswith(".txt") or f.endswith(".py"))]:
                    file = os.path.join(dirpath, filename)
                    if "I3DRobotics_gui_draft_10_StreamService_pointCloud.py" in file:
                        self.pointCloudPyScript = file
                    if file_to_check in file:
                         return True
        return False
                
    def setupFile(self):
        while True:
            self.sessionId = random.randint(10000000000,99999999999)
            if not(self.file_exists(f"{self.sessionId}")):
                break
        #self.sessionSetPath = os.path.join(self.pcDataFolder,f"{self.sessionId}.txt")
        #with open(self.sessionSetPath, "w") as f:
        #    f.write(f"session:{self.sessionId}")

    def __init__(self, widget, parent):
        super(Stream, self).__init__()
        self.parentWidget = widget
        self.parent = parent

        # Updating Structure
        self.layout = QHBoxLayout()
        self.parentWidget.setLayout(self.layout)
        self.left_widget = QLabel()
        self.right_widget = QLabel()
        self
        self.maxFrameWidth = self.left_widget.width()
        self.layout.addWidget(self.left_widget)
        self.layout.addWidget(self.right_widget)

        # Reset param
        self.reset_parameters(True)
        #self.pc_tbdl_widget = QWidget()
        #self.pc_tbdl_widget.hide()
        #self.pc_Window_stream = streamPC()
        #layout.addWidget(self.pc_Window_stream)
        #self.pc_Window_stream.hide()

        #self.fig = plt.figure()
        #self.ax = plt.axes(projection='3d')
        #self.fig.show()
        #plt.show()
        return
    
    def run(self):
        except_counter = 0
        while self.infinitie_loop_bool:
            try:
                #print("Stream initiated")
                while self.pause:
                    time.sleep(1)
                #print("Starting stream")
                pass

                # Connect camera and start data capture
                #print("Connecting to camera...")
                ret = self.deviceCam.connect()
                self.deviceCam.enableHardwareTrigger(False)
                if (ret):
                    self.deviceCam.startCapture()

                    # Set camera exposure value
                    self.deviceCam.setExposure(self.exposure_value)
                    #print("Running camera capture...")

                    while self.deviceCam.isConnected():
                        read_result = self.deviceCam.read()
                        if read_result.valid:
                            # Rectify stereo image pair
                            self.img_left_raw = read_result.left
                            self.img_right_raw = read_result.right
                            if not(self.stream_rectify_var):
                                #cv2.imshow("left", self.img_left_raw)
                                #cv2.imshow("right", self.img_right_raw)
                                #cv2.waitKey(1)
                                self.update_Stream_frame_img([self.img_left_raw,self.img_right_raw])
                                if self.record_data_bool:
                                    self.record_data(1)
                            if self.stream_rectify_var:
                                rect_image_pair = self.calibration.rectify(self.img_left_raw, self.img_right_raw)
                                self.rect_img_left = rect_image_pair.left
                                self.rect_img_right = rect_image_pair.right

                                img_left = phase.scaleImage(self.rect_img_left, self.display_downsample*self.downsample_factor)
                                img_right = phase.scaleImage(self.rect_img_right, self.display_downsample*self.downsample_factor)
                            if (self.stream_rectify_var and not(self.stream_stereo_var)):
                                self.update_Stream_frame_img([img_left,img_right])
                                if self.record_data_bool:
                                    self.record_data(2)
                            if self.stream_stereo_var: 
                                #print(self.stream_stereo_var)
                                match_result = self.matcher.compute(self.rect_img_left, self.rect_img_right)
                            # Check compute is valid
                                if not match_result.valid:
                                    print("Failed to compute match")
                                
                                # Find the disparity from matcher   
                                disparity = match_result.disparity

                                # Convert disparity into 3D pointcloud
                                self.xyz = phase.disparity2xyz(disparity, self.calibration.getQ())
                                self.img_disp = phase.scaleImage(phase.normaliseDisparity(disparity), self.display_downsample)
                                
                                if not(self.point_cloud):
                                    # Display stereo and disparity images
                                    self.update_Stream_frame_img([img_left,self.img_disp])
                                    if self.record_data_bool:
                                        self.record_data(3)
                                else:
                                    if (self.vis == False):
                                        self.vis = o3d.visualization.VisualizerWithEditing()
                                        self.vis.create_window(width=800, height=600)
                                    #file_name = os.path.join(self.pcDataFolder,f"pointCloud dataset _ {self.sessionId} _{time.time()}.ply")
                                    file_name = os.path.join(self.pcDataFolder,"pointCloud_dataset.ply")
                                    save_success = phase.savePLY(file_name, self.xyz, self.rect_img_left)
                                    if self.record_data_bool:
                                        self.record_data(4)
                                    if (save_success):
                                        pcd = o3d.io.read_point_cloud(file_name)
                                        self.vis.clear_geometries()
                                        self.vis.add_geometry(pcd)
                                        self.vis.update_geometry(pcd)
                                        self.vis.update_renderer()
                                        self.vis.poll_events()

                                        #self.run3DSim()
                                    #spcw(xyz)
                                    #self.plot3Ddata(xyz)
                                    #self.pc_tbdl_widget = streamPC(self.parentWidget.width(),self.parentWidget.height())
                                    #self.layout.addWidget(self.pc_tbdl_widget)
                                    ##print("5 HERE")
                                    #self.update_Stream_frame_img(xyz,"single")

                        else:
                            self.deviceCam.disconnect()
                            raise Exception("Failed to read stereo result")
                        if self.pause:
                            self.deviceCam.disconnect()
                            #out.release()
                            #out2.release()
                            break
                except_counter = 0
            except Exception as e:
                except_counter += 1
                if except_counter <5:
                    print(str(e))
                else:
                    raise Exception(str(e))
        
        return

    def update_Device(self, chosenCamClass=False):
        if (chosenCamClass == False):
            self.reset_parameters(True)
        else:
            # Create stereo camera
            if chosenCamClass.name == "Titania":
                self.deviceCam = phase.stereocamera.TitaniaStereoCamera(chosenCamClass.device)
            elif chosenCamClass.name == "Phobos":
                self.deviceCam = phase.stereocamera.PhobosStereoCamera(chosenCamClass.device)
            else:
                raise Exception("Device type unknown")
        return
    
    def reset_parameters(self, bool=False):
        if (bool):
            # Default param
            self.infinitie_loop_bool = True
            self.pause = True
            self.frameToUpdateImg_width = 0

            # Which to display
            self.stream_rectify_var = False
            self.stream_stereo_var = False
            self.point_cloud = False
            self.frame_quantity = 2
            
            self.setupFile()
        return
    
    def update_Stream_frame_img(self, frame):
        if (self.frame_quantity == 2):
            _, _, frame_to_update_left = self.cv2Qimg(frame[0], True)
            self.labelWidth, self.labelHeight, frame_to_update_right = self.cv2Qimg(frame[1], True)
            self.left_widget.setPixmap(QPixmap.fromImage(frame_to_update_left))
            self.right_widget.setPixmap(QPixmap.fromImage(frame_to_update_right))
        return
    
    def cv2Qimg(self, frame, shorten):
        frame_height, frame_width, _ = frame.shape
        width = self.parentWidget.width()-50
        height = round(width*(frame_height/frame_width))
        if shorten:
            width = round(width*0.5)
            height = round(height*0.5)
            
        self.frameToUpdateImg_width_target = width
        frame = cv2.resize(frame,(width,height), cv2.INTER_AREA)
        bytesPerLine = 3*width
        return width,height, QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
    
    def setup_raw(self):
        self.stream_rectify_var = False
        self.stream_stereo_var = False
        self.point_cloud = False
        return
    
    def setup_rectifier(self, left_yaml, right_yaml):
        self.calibration = phase.calib.StereoCameraCalibration.calibrationFromYAML(left_yaml, right_yaml)
        self.stream_rectify_var = True
        self.stream_stereo_var = False
        self.point_cloud = False
        #print("Mode: Rectifier")
        return
    
    def setup_stereo(self):
        self.stream_rectify_var = True
        self.stream_stereo_var = True
        self.point_cloud = False

        # Check for I3DRSGM license
        license_valid = phase.stereomatcher.StereoI3DRSGM().isLicenseValid()
        if license_valid:
            #print("I3DRSGM license accepted")
            stereo_params = phase.stereomatcher.StereoParams(
                phase.stereomatcher.StereoMatcherType.STEREO_MATCHER_I3DRSGM,
                9, 0, 49, False
            )
        else:
            #print("Missing or invalid I3DRSGM license. Will use StereoBM")
            stereo_params = phase.stereomatcher.StereoParams(
                phase.stereomatcher.StereoMatcherType.STEREO_MATCHER_BM,
                11, 0, 25, False
            )

        self.matcher = phase.stereomatcher.createStereoMatcher(stereo_params)
        #print("Mode: Stereo")
        return True
    
    def setup_pointCloud(self):
        self.stream_rectify_var = True
        self.stream_stereo_var = True
        self.point_cloud = True
        return
        
    
    def WindowresizeEvent(self):
        dw = 15
        width = self.parentWidget.width()-25
        if self.frame_quantity == 2:
            width = width*0.5
        if not(self.labelWidth-dw <= width <= self.labelWidth+dw):
            self.left_widget.resize(self.labelWidth,self.labelHeight)
            self.right_widget.resize(self.labelWidth,self.labelHeight)

    def run3DSim(self):
        #print(self.pointCloudPyScript)
        if not(self.pcSimStarted):
            self.pcSimStarted = True
            #print(self.pointCloudPyScript)
            #os.spawnv(os.P_NOWAIT, f"python {self.pointCloudPyScript}", [f"-i {self.sessionId}", f"-f {self.pcDataFolder}", "-s True"])
        return
    
    def changeExposure(self, exposure):
        self.deviceCam.setExposure(exposure)
        return
    
    def capture_data(self, capture):
        fileFolder = self.pcDataFolder
        tme = time.time()
        if not(self.stream_rectify_var):
            filename_left_raw = os.path.join(fileFolder,f"left_raw_{tme}.png")
            filename_right_raw = os.path.join(fileFolder,f"right_raw_{tme}.png")
            cv2.imwrite(filename_left_raw, self.img_left_raw)
            cv2.imwrite(filename_right_raw, self.img_right_raw)
            return True
        elif not(self.stream_stereo_var):
            filename_left_rectify = os.path.join(fileFolder,f"left_rectify_{tme}.png")
            filename_right_rectify = os.path.join(fileFolder,f"right_rectify_{tme}.png")
            cv2.imwrite(filename_left_rectify, self.rect_img_left)
            cv2.imwrite(filename_right_rectify, self.rect_img_right)
            return True
        elif not(self.point_cloud):
            filename_stereo = os.path.join(fileFolder,f"stereo_{tme}.png")
            cv2.imwrite(filename_stereo,self.img_disp)
            return True
        elif self.point_cloud:
            filename_pointcloud = os.path.join(fileFolder,f"pointCloud_{tme}.ply")
            while not(phase.savePLY(filename_pointcloud, self.xyz, self.rect_img_left)):
                print("Attempting...")
                time.sleep(1)
            return True
        return False
    
    def record_data(self, id):
        fileFolder = self.pcDataFolder
        tme = time.time()
        if id>=1:
            print("Saving raw")
            filename_left_raw = os.path.join(fileFolder,f"left_raw_{tme}.png")
            filename_right_raw = os.path.join(fileFolder,f"right_raw_{tme}.png")
            cv2.imwrite(filename_left_raw, self.img_left_raw)
            cv2.imwrite(filename_right_raw, self.img_right_raw)
        if id>=2:
            print("Saving Rectified")
            filename_left_rectify = os.path.join(fileFolder,f"left_rectify_{tme}.png")
            filename_right_rectify = os.path.join(fileFolder,f"right_rectify_{tme}.png")
            cv2.imwrite(filename_left_rectify, self.rect_img_left)
            cv2.imwrite(filename_right_rectify, self.rect_img_right)
        if id>=3:
            print("Saving Stereo")
            filename_stereo = os.path.join(fileFolder,f"stereo_{tme}.png")
            cv2.imwrite(filename_stereo,self.img_disp)
        if id>=4:
            print("Saving Point cloud")
            filename_pointcloud = os.path.join(fileFolder,f"pointCloud_{tme}.ply")
            while not(phase.savePLY(filename_pointcloud, self.xyz, self.rect_img_left)):
                print("Attempting...")
                time.sleep(1)
        return False
