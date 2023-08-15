# I3DRobotics_gui
GUI for Phobos and Titania

dependencies:
  pip install pyqt5-tools opencv-python open3d numpy
  pip install phase
  follow the link to download phase, if the above doesnt work.https://github.com/i3drobotics/pyphase

run 
  git clone https://github.com/AnojanCherry/I3DRobotics_gui.git
  then run the "RunMe.py"

check for a device by refreshing, select a device in the dropdown menu, press connect to connect to it. Ensure the yaml file are downloaded

Run either one of the following command
pyinstaller.exe --onefile --windowed .\I3DRobotics_TP.py
pyinstaller.exe --onefile --windowed --icon=eye.ico .\I3DRobotics_TP.py
https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-linux-pyinstaller/
