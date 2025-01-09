import sys
from PyQt5.QtWidgets import (
    QApplication,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel
)
from src.realtime_swap import RealTimeFaceSwapTab  
from src.image_swap import ImageSwapTab       
from src.face_swap import FaceSwapper         

class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Swapper Application")
        self.setGeometry(100, 100, 1200, 1000) 

        self.face_swapper = FaceSwapper()  

        # Add tabs
        self.addTab(self.real_time_tab(), "Real-Time Face Swap")
        self.addTab(self.image_tab(), "Image Face Swap")
        self.addTab(self.synthetic_tab(), "Generate Synthetic Face")

    def real_time_tab(self):
        """Creates the Real-Time Face Swap tab."""
        real_time_widget = RealTimeFaceSwapTab(self.face_swapper)
        return real_time_widget

    def image_tab(self):
        """Creates the Image Face Swap tab."""
        image_swap_widget = ImageSwapTab()
        return image_swap_widget

    def synthetic_tab(self):
        """Creates the Generate Synthetic Face tab."""
        synthetic_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Synthetic Face Generation Coming Soon!"))
        synthetic_widget.setLayout(layout)
        return synthetic_widget

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
