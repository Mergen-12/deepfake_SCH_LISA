import cv2
from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QLabel, 
    QPushButton, 
    QTextEdit, 
    QMessageBox, 
    QFileDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

class RealTimeFaceSwapTab(QWidget):
    def __init__(self, face_swapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.face_swapper = face_swapper  
        self.cap = self.face_swapper.cap  
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.setup_ui()  

    def setup_ui(self):
        """Sets up the user interface."""
        layout = QVBoxLayout(self)

        # Title or header label
        self.swap_label = QLabel("Real-Time Face Swapper")
        self.swap_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.swap_label)

        # Video feed display
        self.video_feed_label = QLabel()
        self.video_feed_label.setFixedSize(640, 480)  # Adjust to desired video resolution
        self.video_feed_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.video_feed_label, alignment=Qt.AlignCenter)

        # Button to select the source image
        self.select_image_button = QPushButton("Select Source Image")
        self.select_image_button.clicked.connect(self.select_source_image)
        layout.addWidget(self.select_image_button)

        # Start button to start the real-time face swap
        self.start_button = QPushButton("Start Face Swapping")
        self.start_button.clicked.connect(self.start_swapping)
        layout.addWidget(self.start_button)

        # Stop button to stop the real-time face swap
        self.stop_button = QPushButton("Stop Face Swapping")
        self.stop_button.clicked.connect(self.stop_swapping)
        self.stop_button.setEnabled(False)  # Initially disabled
        layout.addWidget(self.stop_button)

        # Console log
        self.console_log = QTextEdit()
        self.console_log.setReadOnly(True)
        layout.addWidget(self.console_log)

        # Toggle console visibility
        self.toggle_console_button = QPushButton("Toggle Console")
        self.toggle_console_button.clicked.connect(self.toggle_console)
        layout.addWidget(self.toggle_console_button)

        self.setLayout(layout)

    def select_source_image(self):
        """Opens a file dialog to select a source image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Source Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.face_swapper.set_src_image(cv2.imread(file_path))
            self.log_message(f"Source image set: {file_path}")
        else:
            self.log_message("No image selected.")

    def update_frame(self):
        """Updates the video feed with face-swapping applied."""
        ret, frame = self.cap.read()
        if not ret:
            self.log_message("Failed to capture frame.")
            self.stop_swapping()
            return

        # Process frame and display it
        result_frame = self.face_swapper.process_frame(frame)
        height, width, channel = result_frame.shape
        bytes_per_line = channel * width
        qimage = QImage(result_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.video_feed_label.setPixmap(QPixmap.fromImage(qimage))

    def start_swapping(self):
        """Starts the real-time face-swapping."""
        if self.face_swapper.src_image is None:
            QMessageBox.warning(self, "Warning", "Please select a source image before starting face swapping.")
            return

        if not self.timer.isActive():  # Ensure only one timer instance
            self.timer.start(30)  # ~30 FPS
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.log_message("Real-time face swapping started.")

    def stop_swapping(self):
        """Stops the real-time face-swapping."""
        if self.timer.isActive():  # Only stop if the timer is running
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.log_message("Real-time face swapping stopped.")

    def log_message(self, message):
        """Logs a message to the console."""
        self.console_log.append(message)
        self.console_log.moveCursor(self.console_log.textCursor().End)

    def toggle_console(self):
        """Toggles the visibility of the console log."""
        self.console_log.setVisible(not self.console_log.isVisible())

    def closeEvent(self, event):
        """Handles the window close event."""
        self.stop_swapping()
        event.accept()
