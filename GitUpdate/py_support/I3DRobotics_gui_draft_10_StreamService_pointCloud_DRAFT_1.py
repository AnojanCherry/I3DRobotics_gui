import typing
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QObject

from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QApplication, QMainWindow
)

import open3d as o3d
import win32gui
import sys, time

# https://github.com/isl-org/Open3D/discussions/4668
class stream_point_cloud(QWidget):
    def __init__(self):
        self.thread = stream_point_cloud_thread()
        self.running = False
        return
    
    def update(self, width, height):
        if self.running:
            self.thread.stop()
            self.running = False
        
        self.thread.updateParam(width, height)
        self.thread.start()
        self.running = True
        return

class stream_point_cloud_thread(QtCore.QThread):
    def __init__(self):
        super(stream_point_cloud_thread, self).__init__()
        return
    
    def updateParam(self, width, height):
        self.width = width
        self.height = height
        return
    
    def run(self):
        print("Updating")
        worker = stream_point_cloud_worker(self.width, self.height)
        time.sleep(3)
        return
    
    def stop(self):
        self.terminate()


class stream_point_cloud_worker(QWidget):
    def __init__(self, width, height):
        super(stream_point_cloud_worker, self).__init__()
        pcp = "C:\\Users\\I3DRStudent\\Documents\\AnojanCherry\\i3dRobotics_gui\\GitUpdate\\ui2py\\1.ply"
        self.resize(width,height)
        layout = QGridLayout(self)

        pcd = o3d.io.read_point_cloud(pcp)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(pcd)
        
        print("Stuck")
        hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        print("Stuck")
        self.window = QtGui.QWindow.fromWinId(hwnd)    
        print("Stuck")
        self.windowcontainer = QMainWindow.createWindowContainer(self.window, self)
        print("Stuck")
        layout.addWidget(self.windowcontainer, 0, 0)
        print("Stuck")
        timer = QtCore.QTimer(self)
        print("Stuck")
        timer.timeout.connect(self.update_vis)
        print("Stuck")
        timer.start(1)
        print("Stuck")
        self.show()

    def update_vis(self):
        #self.vis.update_geometry()
        self.vis.poll_events()
        self.vis.update_renderer()

    

if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = stream_point_cloud()
    form.update(600,500)
    #form.setWindowTitle('o3d Embed')
    #form.setGeometry(100, 100, 600, 500)
    #form.show()
    sys.exit(app.exec_())