# B0sh - This was written with ~20 chat gpt 4 question responses. 
# It didn't get it right the first time on a lot of features, but
# with my programming knowledge and asking follow up questions it 
# mostly got there in the end. Going hunting with google felt
# like a complete waste of time in comparison.
# 
# IF I was to do this on my own, I would have ended up on some how
# to make python GUIs tutorial page and had to research every one 
# of these 150 lines in incredible detail
# Instead I got through to the working prototype phase in 20 minutes, and 
# did all of my polish in another 40. Undenibly mind blowing.
# 5/19/2023 -B0sh

# pip install pyqt5 pillow watchdog

import os
import sys
import shutil
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QSizePolicy, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QPushButton, QFileDialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

ICON_SIZE = 64
EXTENSION = ".png"


class AspectRatioPixmapLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setScaledContents(False)
        self._pixmap = None

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  # Add this line


    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        if self._pixmap is not None:
            super().setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def resizeEvent(self, event):
        if self._pixmap is not None:
            super().setPixmap(self._pixmap.scaled(event.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


class ImageList(QListWidget):
    def __init__(self, window,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reordering = False
        self.error = False
        self.window = window

        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))  # adjust the numbers based on the preferred icon size
        self.setDragDropMode(QListWidget.InternalMove)
        self.setFlow(QListWidget.LeftToRight)  # Make the list horizontal
        self.setWrapping(False)
        self.setWordWrap(True)  # Enable word wrapping for the text
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Add horizontal scrollbar

    def dropEvent(self, event):
        super().dropEvent(event)
        self.reorder_images()

    def reorder_images(self):
        if self.reordering == True:
            self.error = True
            return False
        
        self.reordering = True

        images_dir = self.window.images_dir

        # Backup files before reordering.
        backup_dir = os.path.join(images_dir, "backup")
        os.makedirs(backup_dir, exist_ok=True)
        for image in os.listdir(self.window.images_dir):
            if image.endswith(EXTENSION):
                shutil.copy2(os.path.join(images_dir, image), backup_dir)

        # Rename all files to temporary names.
        for i in range(self.count()):
            item = self.item(i)
            os.rename(os.path.join(images_dir, item.text()) + EXTENSION, os.path.join(images_dir, f"temp_{i + 1}{EXTENSION}"))

        # Rename files to their new names.
        temp_images = sorted([f for f in os.listdir(images_dir) if f.startswith("temp_")], key=lambda x: int(os.path.splitext(x)[0].split("_")[1]))
        for i, image in enumerate(temp_images):
            os.rename(os.path.join(images_dir, image), os.path.join(images_dir, f"{i + 1}{EXTENSION}"))

        if self.error == True:
            raise "Double image reorder attempted"

        self.reordering = False

        self.window.update_images()


class MainWindow(QMainWindow):
    def __init__(self, images_dir, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.image_list = ImageList(self)
        self.image_list.itemSelectionChanged.connect(self.show_selected_image)  # Connect the selection changed signal to the function
        self.image_list.setFixedHeight(ICON_SIZE + 10)

        self.image_label = AspectRatioPixmapLabel() 

        self.select_dir_button = QPushButton("Select folder")  # Create the button
        self.select_dir_button.setMaximumWidth(200)
        self.select_dir_button.clicked.connect(self.select_directory)  # Connect the button to the function

        self.main_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.select_dir_button)  # Add the button to the layout
        self.layout.addWidget(self.image_list)
        self.layout.addWidget(self.image_label)  # Add the QLabel to the layout
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Walden's World of Minecraft (tm) Powerpoint Mod Image Processor (powered by Chat GPT)")

        self.resize(1600, 800)
        # self.setMinimumSize(QSize(600, 0))
        # self.setMaximumHeight(200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.update_directory(images_dir)


    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select directory", self.images_dir)  # Open the dialog
        if directory:  
            self.update_directory(directory)


    def update_directory(self, directory):
        if not os.path.isdir(directory):
            self.images_dir = ""
            self.update_images()
            return

        files = os.listdir(directory)
        for file in files:
            if os.path.isfile(os.path.join(directory, file)):
                # Check if the file is an image file with a numeric name
                name, ext = os.path.splitext(file)
                if ext != EXTENSION or not name.isdigit():
                    QMessageBox.warning(self, "Invalid directory", "The selected directory contains invalid files.")
                    self.images_dir = ""
                    self.update_images()
                    return

        self.images_dir = directory  
        self.update_images()  # Update the image list

    def update_images(self):
        self.image_list.clear()
        if os.path.isdir(self.images_dir):
            images = sorted([f for f in os.listdir(self.images_dir) if f.endswith(EXTENSION)], key=lambda x: int(os.path.splitext(x)[0]))

            for image in images:
                pixmap = QPixmap(os.path.join(self.images_dir, image))
                icon = QIcon(pixmap)
                item = QListWidgetItem(icon, image.replace(EXTENSION, ""))
                self.image_list.addItem(item)

    def show_selected_image(self):
        items = self.image_list.selectedItems()
        if items:
            item = items[0]
            image_file = os.path.join(self.images_dir, item.text()) + EXTENSION
            self.image_label.setPixmap(QPixmap(image_file))  # Set the QLabel's pixmap


if __name__ == "__main__":
    images_dir = sys.argv[1] if len(sys.argv) > 1 else ""

    app = QApplication([])
    window = MainWindow(images_dir)
    window.show()
    app.exec_()
