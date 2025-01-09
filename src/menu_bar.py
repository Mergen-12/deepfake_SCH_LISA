from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog, QMessageBox

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.create_menu_bar()

    def create_menu_bar(self):
        # File menu
        file_menu = self.addMenu("File")
        
        open_action = QAction("Open Image", self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        save_action = QAction("Save Result", self)
        save_action.triggered.connect(self.save_result)
        file_menu.addAction(save_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = self.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.redo_action)
        edit_menu.addAction(redo_action)

        # View menu
        view_menu = self.addMenu("View")
        
        toggle_console_action = QAction("Toggle Console", self)
        toggle_console_action.triggered.connect(self.parent.toggle_console)
        view_menu.addAction(toggle_console_action)

        # Help menu
        help_menu = self.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        user_guide_action = QAction("User Guide", self)
        user_guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(user_guide_action)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.parent.log_message(f"Opened image: {file_name}")
            # You'll need to implement the logic to load the image into your face swapper

    def save_result(self):
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save Result", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.parent.log_message(f"Saved result to: {file_name}")
            # You'll need to implement the logic to save the current result

    def undo_action(self):
        self.parent.log_message("Undo action performed")
        # Implement undo functionality

    def redo_action(self):
        self.parent.log_message("Redo action performed")
        # Implement redo functionality

    def show_about(self):
        QMessageBox.about(self.parent, "About Face Swapper", "Face Swapper v1.0\nCreated by [Your Name]\n\nA powerful tool for real-time face swapping and image manipulation.")

    def show_user_guide(self):
        QMessageBox.information(self.parent, "User Guide", "1. Use 'Open Image' to load a source image.\n2. Click 'Start' to begin real-time face swapping.\n3. Use the controls on the right to adjust parameters.\n4. Click 'Stop' to pause the face swapping.\n5. Use 'Save Result' to save the current output.")