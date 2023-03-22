from threading import Thread
import gi
import time
from gi.repository import Gst, GLib

gi.require_version(
    "Gst", "1.0"
)  # Set the required version of Gst (GStreamer) in the gi module

# Function to create the GStreamer pipeline for a camera stream
def create_pipeline(multicast_group, port):
    # Return a new GStreamer pipeline using the provided multicast group and port
    return Gst.parse_launch(
        f"udpsrc multicast-group={multicast_group} auto-multicast=true port={port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! autovideosink sync=false"
    )


# Function to run the GStreamer pipeline and handle stopping it
def run_pipeline(pipeline, main_loop):

    pipeline.set_state(Gst.State.PLAYING)  # Set the pipeline state to PLAYING

    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:  # If the user presses Ctrl+C, break the loop
        pass

    finally:
        pipeline.set_state(
            Gst.State.NULL
        )  # Ensure that the pipeline stops and the main loop quits when the loop is broken
        main_loop.quit()


# Function to set up and run a camera stream with GStreamer
def camera_stream(multicast_group, port):

    Gst.init()  # Initialize GStreamer

    main_loop = GLib.MainLoop()  # Create a new GLib main loop

    pipeline = create_pipeline(
        multicast_group, port
    )  # Create a new GStreamer pipeline using the provided multicast group and port

    thread = Thread(
        target=main_loop.run
    )  # Start the GLib main loop in a separate thread
    thread.start()

    run_pipeline(
        pipeline, main_loop
    )  # Run the GStreamer pipeline and handle stopping it


# Camera stream information (multicast group and port)
camera1_info = ("224.1.1.1", 5000)
camera2_info = ("224.1.1.1", 5001)

# Create and start threads to run both camera streams concurrently
thread1 = Thread(target=camera_stream, args=camera1_info)
thread2 = Thread(target=camera_stream, args=camera2_info)

# Start the threads
thread1.start()
thread2.start()

# Wait for the first and second camera stream thread to finish
thread1.join()
thread2.join()
