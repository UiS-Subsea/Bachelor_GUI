from threading import Thread

import gi

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib
import time

Gst.init()

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()


pipeline = Gst.parse_launch(
    "udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! autovideosink sync=false"
)
pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
