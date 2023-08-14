from PyQt5.QtCore import QThread
from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d

import os, optparse, threading, time

class stream_point_cloud_worker():
    def __init__(self, sessioId, folder_path):
        super(stream_point_cloud_worker, self).__init__()

        self.sessionId = sessioId
        self.folderPath = folder_path

        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        self.fig.show()
        return
    
    def update(self,x,y,z):
        self.ax.cla()
        print("Dare")
        self.ax.scatter3D(x, y, z)
        print("Daring")
        plt.draw()
        print("dared")
        plt.pause(0.1)
        print("Ended dare")
        return
    
    def get_new_data(self):
        noNewData = True
        lst=[]
        while noNewData:
            print("Checking")
            lst.clear()
            for root, dirs, files in os.walk(self.folderPath):
                for name in files:
                    if str(self.sessionId) in name:
                        lst.append(os.path.join(root,name))
                        noNewData = False
            lst.sort()
            time.sleep(1)
        file_chosen = lst[0]
        data = np.load(file_chosen, allow_pickle=True)
        file_new = str(file_chosen).replace(str(self.sessionId),"readed")
        os.replace(file_chosen, file_new)
        return data[:,:,0], data[:,:,1], data[:,:,2]
    
    def thread_func(self):
        while True:
            x,y,z = self.get_new_data()
            self.update(x,y,z)
        return

def displayO3D(file):
    #cloud = o3d.io.read_point_cloud(file) # Read point cloud
    cloud = o3d.io.read_point_cloud(file)
    vis.update_geometry(cloud)    # Visualize point cloud   
    vis.poll_events()
    vis.update_renderer()

def updateVisualiser(file):
    input("Hello")
    return
    #vis.Visualizer.clear_geometries(o3d.cpu.pybind.visualization.Visualizer)


def get_file_name():
    noNewData = True
    path = ""
    lst = []

    for root, dirs, files in os.walk(sourcefolder):
          for name in files:
              if str(sessionId) in name:
                lst.append(os.path.join(root,name))
                noNewData = False
        
    if not(noNewData):
        lst.sort()
        path = lst[0]

    return noNewData, path

ev = o3d.visualization.ExternalVisualizer()
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.clear_geometries()
vis.poll_events()
input("Hello")

if __name__ == '__main__':
    #print(sys.argv)
    parse = optparse.OptionParser()
    parse.add_option("-i", "--session_id", default="001", dest="sessionId")
    parse.add_option("-s", "--stream", default=True, dest="streamService")
    parse.add_option("-f", "--Folder", default="C:\\Users\\I3DRStudent\\Documents\\AnojanCherry\\i3dRobotics_gui\\GitUpdate\\py_support\\misc", dest="sourceFolder")
    options, arguments = parse.parse_args()
    print(options)
    sessionId = options.sessionId
    sourcefolder = options.sourceFolder
    stream = options.streamService
    #input(stream)

    path_truth, path = get_file_name()
    #vis.
    #vis.create_window(width=640, height=480)
    #frame = o3d.geometry.TriangleMesh.create_coordinate_frame(1.5)
    #mesh = o3d.geometry.TriangleMesh.create_sphere()
    #vis.add_geometry(frame)
    #vis.add_geometry(mesh)

    if not(path_truth):
        displayO3D(path)
        time.sleep(3)
    print("Updating")
    updateVisualiser("")

    '''
    if stream:
        displayO3D()

    while stream:
        noNewData = True
        lst=[]
        while noNewData:
            print("Checking")
            lst.clear()
            for root, dirs, files in os.walk(sourcefolder):
                #print(files)
                for name in files:
                    if str(sessionId) in name:
                        lst.append(os.path.join(root,name))
                        noNewData = False
            lst.sort()
            time.sleep(1)
        file_chosen = lst[0]
        data = np.load(file_chosen, allow_pickle=True)
        file_new = str(file_chosen).replace(str(sessionId),"readed")
        os.replace(file_chosen, file_new)
        x,y,z = data[:,:,0], data[:,:,1], data[:,:,2]
        
        ax.cla()
        print("Dare")
        ax.scatter3D(x, y, z)
        print("Daring")
        plt.draw()
        print("dared")
        #plt.pause(5)
        print("Ended dare")
        break
        '''

#input("Hello")