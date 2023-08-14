import open3d as o3d

import optparse, os, time, random
'''
class Viewer():
    def __init__(self, sourcefolder):
        self.sourcefolder = sourcefolder
        self.viz = o3d.visualization.Visualizer()
        self.viz.create_window(width=800,height=600)
        self.viz.poll_events()
        self.viz.update_renderer()
        #self.thread = threading()
        return
    
    def get_file_name(self):
        noNewData = True
        path = ""
        lst = []

        for root, dirs, files in os.walk(self.sourcefolder):
            for name in files:
                if (str(sessionId) in name) and (".ply" in name):
                    lst.append(os.path.join(root,name))
                    pathlst = name.split("_")
                    path_new = pathlst[0]+"_READED_"+pathlst[2]
                    path_new = os.path.join(root,path_new)
                    noNewData = False
            
        if not(noNewData):
            lst.sort()
            path = lst[0]
            print(path_new)
            os.replace(path,path_new)

        return noNewData, path
    
    def update_frame(self, path):
        self.cloud = o3d.io.read_point_cloud(path)
        #self.viz.clear_geometries()
        #self.viz.poll_events()
        #self.viz.update_renderer()
        #self.viz.update_geometry(cloud)
        self.viz.add_geometry(self.cloud, True)
        self.viz.poll_events()
        self.viz.update_renderer()
        return
    
    def update_frame_regular(self, path):
        self.viz.remove_geometry(self.cloud, False)
        self.cloud = o3d.io.read_point_cloud(path)
        #self.viz.clear_geometries()
        #self.viz.poll_events()
        #self.viz.update_renderer()
        #self.viz.update_geometry(cloud)
        self.viz.add_geometry(self.cloud, False)
        self.viz.poll_events()
        self.viz.update_renderer()
        return
    
    def run(self):
        while True:
            path_truth, path = self.get_file_name()
            if not(path_truth):
                self.update_frame_regular(path)
            time.sleep(1)

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

    disp = Viewer(sourcefolder)

    path_truth = True
    while path_truth:
        path_truth, path = disp.get_file_name()
        if not(path_truth):
            disp.update_frame(path)
            break

    disp.run()import open3d as o3d

    '''
# Create an empty visualization window
vis = o3d.visualization.Visualizer()
vis.create_window()
sessionId = ""
sourcefolder = "C:\\Users\\I3DRStudent\\Documents\\AnojanCherry\\i3dRobotics_gui\\GitUpdate\\py_support\\misc"
def get_live_point_cloud_data():
        noNewData = True
        path = ""
        lst = []

        for root, dirs, files in os.walk(sourcefolder):
            for name in files:
                if (str(sessionId) in name) and (".ply" in name):
                    lst.append(os.path.join(root,name))
                    pathlst = name.split("_")
                    path_new = str(9)+pathlst[0]+"_9002_"+str(random.randint(1,7423656734))+pathlst[-1]
                    path_new = os.path.join(root,path_new)
                    noNewData = False
            
        if not(noNewData):
            lst.sort()
            path = lst[0]
            print(path_new)
            os.replace(path,path_new)

        return noNewData, path_new

while True:
    # Get live streaming point cloud data (replace with your data source)
    tt, live_point_cloud = get_live_point_cloud_data()
    print(live_point_cloud)

    if not(tt):
        print("Updating")
        # Convert live point cloud data to Open3D point cloud object
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.io.read_point_cloud(live_point_cloud) #o3d.utility.Vector3dVector(live_point_cloud)

        # Update the visualization with the new point cloud
        vis.clear_geometries()
        vis.add_geometry(pcd)
        vis.update_geometry(pcd)
        vis.poll_events()
        vis.update_renderer()
        input("Enter to conitnue")

# Close the visualization window when done
vis.destroy_window()