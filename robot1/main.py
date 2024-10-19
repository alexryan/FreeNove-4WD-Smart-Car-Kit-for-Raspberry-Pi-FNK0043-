import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from picamera2 import Picamera2
import numpy as np

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raspberry Pi Camera Stream with Arrow Keys")
        self.setGeometry(100, 100, 640, 600)  # Adjust window size

        # Main widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        # Layout for the camera stream and buttons
        self.layout = QVBoxLayout()

        # Camera stream label
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        # Initialize the Picamera2
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))

        # Start the camera
        self.picam2.start()

        # Set up a timer to update the video stream every 100ms (10fps)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)

        # Layout for arrow buttons
        self.button_layout = QHBoxLayout()

        # Create the arrow buttons
        self.up_button = QPushButton("Up", self)
        self.left_button = QPushButton("Left", self)
        self.down_button = QPushButton("Down", self)
        self.right_button = QPushButton("Right", self)

        # Add buttons to the layout
        self.button_layout.addWidget(self.left_button)
        self.button_layout.addWidget(self.up_button)
        self.button_layout.addWidget(self.down_button)
        self.button_layout.addWidget(self.right_button)

        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)

        # Set layout
        self.main_widget.setLayout(self.layout)

        # Connect button clicks to actions (you can add specific actions)
        self.up_button.clicked.connect(lambda: self.button_clicked("Up"))
        self.down_button.clicked.connect(lambda: self.button_clicked("Down"))
        self.left_button.clicked.connect(lambda: self.button_clicked("Left"))
        self.right_button.clicked.connect(lambda: self.button_clicked("Right"))

    def update_frame(self):
        # Capture the frame from the camera as an RGB array
        frame = self.picam2.capture_array()

        # Convert BGR to RGB
        frame_rgb = frame[:, :, ::-1]

        # Convert the NumPy array to bytes
        height, width, channel = frame_rgb.shape
        bytes_per_line = 3 * width
        qt_image = QImage(frame_rgb.data.tobytes(), width, height, bytes_per_line, QImage.Format_RGB888)

        # Set the pixmap to the QLabel
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        # Handle arrow key presses and trigger the corresponding buttons
        if event.key() == Qt.Key_Up:
            self.up_button.click()
        elif event.key() == Qt.Key_Down:
            self.down_button.click()
        elif event.key() == Qt.Key_Left:
            self.left_button.click()
        elif event.key() == Qt.Key_Right:
            self.right_button.click()

    def button_clicked(self, direction):
        print(f"{direction} button clicked")

    def closeEvent(self, event):
        # Ensure the camera process is terminated when the window is closed
        self.picam2.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
