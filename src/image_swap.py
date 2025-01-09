from PyQt5.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QFileDialog, 
    QApplication,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from src.face_swap import FaceSwapper


class ImageSwapTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.source_image_path = None
        self.dest_image_path = None
        
    def initUI(self):
        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create image display section
        image_layout = QHBoxLayout()
        
        # Source image section
        source_section = QVBoxLayout()
        self.source_label = QLabel()
        self.source_label.setFixedSize(320, 320)
        self.source_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #cccccc;
                background-color: white;
            }
        """)
        self.source_label.setAlignment(Qt.AlignCenter)
        self.source_label.setText("Source Image\n(Click to select)")
        
        self.source_button = QPushButton("Select Source Image")
        self.source_button.clicked.connect(self.load_source_image)
        
        source_section.addWidget(QLabel("Source Face:"))
        source_section.addWidget(self.source_label)
        source_section.addWidget(self.source_button)
        
        # Destination image section
        dest_section = QVBoxLayout()
        self.dest_label = QLabel()
        self.dest_label.setFixedSize(320, 320)
        self.dest_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #cccccc;
                background-color: white;
            }
        """)
        self.dest_label.setAlignment(Qt.AlignCenter)
        self.dest_label.setText("Destination Image\n(Click to select)")
        
        self.dest_button = QPushButton("Select Destination Image")
        self.dest_button.clicked.connect(self.load_dest_image)
        
        dest_section.addWidget(QLabel("Destination Face:"))
        dest_section.addWidget(self.dest_label)
        dest_section.addWidget(self.dest_button)
        
        # Add sections to image layout
        image_layout.addLayout(source_section)
        image_layout.addLayout(dest_section)
        
        # Create result section
        result_section = QVBoxLayout()
        self.result_label = QLabel()
        self.result_label.setFixedSize(640, 320)
        self.result_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #cccccc;
                background-color: white;
            }
        """)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setText("Result will appear here")
        
        result_section.addWidget(QLabel("Result:"))
        result_section.addWidget(self.result_label)
        
        # Create control buttons
        button_layout = QHBoxLayout()
        
        self.swap_button = QPushButton("Swap Faces")
        self.swap_button.clicked.connect(self.perform_swap)
        self.swap_button.setEnabled(False)
        
        self.save_button = QPushButton("Save Result")
        self.save_button.clicked.connect(self.save_result)
        self.save_button.setEnabled(False)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all)
        
        button_layout.addWidget(self.swap_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        
        # Add all layouts to main layout
        main_layout.addLayout(image_layout)
        main_layout.addLayout(result_section)
        main_layout.addLayout(button_layout)
        
        self.status_label = QLabel()
        main_layout.addWidget(self.status_label)
        
    def load_source_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Source Image", "", "Image Files (*.jpg *.png)"
        )
        if file_name:
            self.source_image_path = file_name
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(320, 320, Qt.KeepAspectRatio)
            self.source_label.setPixmap(scaled_pixmap)
            self.check_swap_availability()
            
    def load_dest_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Destination Image", "", "Image Files (*.jpg *.png)"
        )
        if file_name:
            self.dest_image_path = file_name
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(320, 320, Qt.KeepAspectRatio)
            self.dest_label.setPixmap(scaled_pixmap)
            self.check_swap_availability()
            
    def check_swap_availability(self):
        self.swap_button.setEnabled(
            self.source_image_path is not None and self.dest_image_path is not None
        )
            
    def perform_swap(self):
        try:
            self.status_label.setText("Processing...")
            QApplication.processEvents()
        
            # Initialize FaceSwapper if not already initialized
            face_swapper = FaceSwapper()
            face_swapper.set_src_image_path(self.source_image_path)  # Dynamically set source image
        
            # Perform the swap
            result = face_swapper.swap_image(self.dest_image_path)
        
            # Convert result to QPixmap and display
            height, width, channel = result.shape
            bytes_per_line = channel * width
            q_image = QImage(result.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(640, 320, Qt.KeepAspectRatio)
            self.result_label.setPixmap(scaled_pixmap)
        
            self.save_button.setEnabled(True)
            self.status_label.setText("Face swap completed successfully!")
        
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            

    def save_result(self):
        if self.result_label.pixmap():
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Save Result", "", "Image Files (*.jpg *.png)"
            )
            if file_name:
                self.result_label.pixmap().save(file_name)
                self.status_label.setText(f"Result saved to {file_name}")
                
    def clear_all(self):
        self.source_image_path = None
        self.dest_image_path = None
        self.source_label.setText("Source Image\n(Click to select)")
        self.dest_label.setText("Destination Image\n(Click to select)")
        self.result_label.setText("Result will appear here")
        self.source_label.setPixmap(QPixmap())
        self.dest_label.setPixmap(QPixmap())
        self.result_label.setPixmap(QPixmap())
        self.swap_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.status_label.setText("")