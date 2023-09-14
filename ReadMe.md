
# I3DRobotics
The objective is to create a simple gui that lets user connect to a Phobos/Titania and display its content to its users, while allowing user to capture/record the data.

### Table of contents
1. [Installation](#installation)
2. [Dependencies](#dependencies)
3. [Running the software](#running-the-software)
    1. [Starting](#starting)
    2. [Record/Capture](#recordcapture)

## Installation
Run the following command in your prefered working directory.
```bash
git clone https://github.com/AnojanCherry/I3DRobotics_gui.git
```
alternatively you can download the files as a zip and extract it to your working directory.

## Dependencies

The project depends on the python libraries such as Phase, pyqt5, opencv, open3d and numpy. To install these run the following command.
```bash
pip install pyqt5-tools opencv-python open3d numpy
```

An alternative way to download phase is provided in the following link.
  https://github.com/i3drobotics/pyphase
    
## Running the software
### Starting
  1. Run the "RunMe.py" to start the program. 
  2. Mount the Phobos/Titania and then press refresh. 
  3. Select the device from the drop down and then press connect. Press again to disconnect.
  4. Ensure that the right.yaml and left.yaml file are in the pysupport folder. Press rectify to rectify (needs yaml files). stereo and point cloud can then be navigated from there. 

  Exposure can be adjusted through out the connection. 

  ### Record/Capture
  Data can be recorded/captured throught the session, these data are then saved in pysupport/misc/*. Time elapsed stamp are printed in the file name.
  
  Catpure - Single shot.<br/>
  Record - Save all data in a continous stream.
## Developer usefulness
```python
python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py
```
