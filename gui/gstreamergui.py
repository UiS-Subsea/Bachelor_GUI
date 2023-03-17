import sys
from threading import Thread

import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstGL", "1.0")

from gi.repository import Gst, GLib, Gtk, GstGL
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QCloseEvent

Gst.init(None)

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GStreamer Video Player")
        self.setGeometry(100, 100, 640, 480)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.installEventFilter(self)

        self.pipeline = Gst.parse_launch("udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! glupload ! glcolorconvert ! qtvideosink sync=false")

        self.sink = self.pipeline.get_by_interface(GstVideo.VideoOverlay)
        self.widget = QWidget(self)
        self.layout.addWidget(self.widget)

        self.pipeline.set_state(Gst.State.PLAYING)

        # Connect the VideoOverlay interface to the widget
        self.sink.set_window_handle(self.widget.winId())

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Close:
            self.stop_pipeline()
            self.main_loop.quit()
        return super().eventFilter(obj, event)

    def stop_pipeline(self):
        self.pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()

    # Use GLib.idle_add() to schedule the main loop in the main thread
    GLib.idle_add(player.pipeline.get_bus().poll, GLib.PRIORITY_DEFAULT)
    app.exec_()
    player.stop_pipeline()