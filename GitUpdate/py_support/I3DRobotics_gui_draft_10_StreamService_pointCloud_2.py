from PyQt5.QtCore import QThread
from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

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

if __name__ == '__main__':
    #print(sys.argv)
    parse = optparse.OptionParser()
    parse.add_option("-i", "--session_id", dest="sessionId")
    parse.add_option("-s", "--stream", default=True, dest="streamService")
    parse.add_option("-f", "--Folder", dest="sourceFolder")
    options, arguments = parse.parse_args()
    sessionId = options.sessionId
    sourcefolder = options.sourceFolder
    print(options)
    print(sessionId)
    
    print("Creating")
    stream = stream_point_cloud_worker(int(sessionId), sourcefolder)
    print("Setted up")
    stream.thread_func()
    #thread = threading.Thread(target=stream.thread_func, args=(1,))
    
    print("starting")
    #thread.start()