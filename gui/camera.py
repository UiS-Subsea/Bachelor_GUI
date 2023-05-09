from threading import Thread
import gi, time
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib

def create_pipeline(multicast_group, port):
  return Gst.parse_launch(f"udpsrc multicast-group={multicast_group} auto-multicast=true port={port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! autovideosink sync=false")

def run_pipeline(pipeline, main_loop):
    pipeline.set_state(Gst.State.PLAYING)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)
        main_loop.quit()

def run_camera_stream(multicast_group, port):
    Gst.init([])
    main_loop = GLib.MainLoop()
    pipeline = create_pipeline(multicast_group, port)
    thread = Thread(target=main_loop.run)
    thread.start()
    run_pipeline(pipeline, main_loop)

camera1_info = ("224.1.1.1", 5000)
camera2_info = ("224.1.1.1", 5001)
camera3_info = ("224.1.1.1", 5002)
camera4_info = ("224.1.1.1", 5003)

thread1 = Thread(target=run_camera_stream, args=camera1_info)
thread2 = Thread(target=run_camera_stream, args=camera2_info)
thread3 = Thread(target=run_camera_stream, args=camera3_info)
thread4 = Thread(target=run_camera_stream, args=camera4_info)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()