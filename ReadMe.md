
# I3DRobotics
The objective is to create a simple gui that lets user connect to a camera and display its content to its users.
To start up either download the files or run the following command in a terminal

## Installation

You can either download the file and extract it in a folder or run the following command to download the files.

```bash
git clone https://github.com/AnojanCherry/I3DRobotics_gui.git
```
### dependencies
The project depends on the python libraries such as Phase, pyqt5, opencv, open3d and numpy. to install these run the following commands.
```bash
pip install pyqt5-tools opencv-python open3d numpy
```

An alternative way to download phase is provided in the following link.
  https://github.com/i3drobotics/pyphase
    
## Running the software
### Starting
  Run the "RunMe.py" to start the program. To search for a connected device press refresh. and to establish a connection and start streaming, presh connect. Press again to disconnect.

  Ensure that right and left yaml file are in the pysupport folder. Press rectify to rectify (needs yaml files). stereo and point cloud can then be navigated from there. 

  Exposure, downsample and sample factor can be adjusted through out the connection. 

  ### Output
  data can be recorded/captured throught the session, these data are then saved in pysupport/misc. Time elapsed stamp are printed in the file name.
