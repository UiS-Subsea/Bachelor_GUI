# Bachelor_GUI

Repo for alle koselige gutter i GUI seksjonen i UiS-Subsea

# Viktige ting om installasjon

QT Designer
Python 3.9
Pyqt5

# Formatering av filer

black {source_file_or_directory}

eksempel:
black D:\Bachelor_GUI

mest sannsynlig berre å bytte ut D med C p diskane dokka <3

# Måten prosjektet skal bli såtte opp

GUI python fil som impoerterer ei UI fil fra QT Designer

# Requirements !

pip install -r requirements.txt

for å oppdatere requirements om du he installert ei ny python pakke i virtual environment (venv)

pip freeze > requirements.txt

# Venv

Powershell:
venv\Scripts\Activate

Mac/Linux:
source venv/bin/activate

# Mac

For å endre venv versjon:
virtualenv -p /path/to/python3.9.6 venv
Brukte:
pip install virtualenv
virtualenv -p /usr/bin/python3 venv



# Koble til jetson og kjøre programmet
ssh jetson@10.0.0.2
canup
(PW: jetson)
sudo route add -net 224.0.0.0 netmask 224.0.0.0 eth0
cd Kommunikasjon-2023/
python3 main.py

# Kjøre på pcen
python3 main.py



#Kjøre kamera
gst-launch-1.0 udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! autovideosink sync=false

#Sette route på pcen

sudo route add -net 224.0.0.0 netmask 224.0.0.0 enp2s0
