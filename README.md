# UiS-Subsea Topside System
This repository contains information on how to connect to the Jetson and run the program, as well as how to run the project from your PC.

# Project Details
The purpose of this program is to enable communication between the topside system and the underwater vehicle. It utilizes a graphical user interface (GUI) to display important information and control the vehicle. The code structure and organization follow standard programming practices.
# Jetson Connection
To connect to the Jetson and run the program, follow these steps:

SSH into the Jetson using the command ssh jetson@10.0.0.2.

Enter the password, which is jetson.

Run the command canup.

Run the command sudo route add -net 224.0.0.0 netmask 224.0.0.0 eth0.

Navigate to the Kommunikasjon-2023/ directory using the command cd Kommunikasjon-2023/.

Finally, run the command python3 main.py to execute the program.

# Program Setup on main pc
Install the required packages by running the command pip install -r requirements.txt.

Run the command sudo route add -net 224.0.0.0 netmask 224.0.0.0 enp2s0.

Finally, run the command python3 main.py to execute the program.

# Camera Streaming
To stream the camera, use the command:

gst-launch-1.0 udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! autovideosink sync=false

You can use ports 5000, 5001, 5002, or 5003.

