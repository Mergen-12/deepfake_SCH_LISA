from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QPushButton

class ControlPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Controls", parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        controls = [
            "Eye Shape",
            "Eyeglasses",
            "Hairstyle",
            "Mouth Open/Closed",
            "Beard",
            "Motion Controls"
        ]

        for control in controls:
            button = QPushButton(control)
            button.clicked.connect(lambda checked, text=control: self.on_control_click(text))
            layout.addWidget(button)

        self.setLayout(layout)

    def on_control_click(self, control_name):
        self.parent.log_message(f"{control_name} control clicked")
        # Implement the specific control functionality here