
# import sys
# import random
# from PyQt6 import QtCore, QtWidgets, QtGui

# class MyWidget(QtWidgets.QWidget):
#        def __init__(self):
#               super().__init__()
#               self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
#               self.button = QtWidgets.QPushButton("Click me!")
#               self.text = QtWidgets.QLabel("Hello World!", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
#               self.layout = QtWidgets.QVBoxLayout(self)
#               self.layout.addWidget(self.text)
#               self.layout.addWidget(self.button)
#               self.button.clicked.connect(self.magic)
#        @QtCore.pyqtSlot()
#        def magic(self):
#               self.text.setText(random.choice(self.hello))

# if __name__ == "__main__":
#        app = QtWidgets.QApplication([])

#        widget = MyWidget()
#        widget.resize(1000, 400)
#        widget.show()

#        sys.exit(app.exec())       
# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


# # class MainWindow(QMainWindow):
# #     def __init__(self):
# #         super().__init__()

# #         self.setWindowTitle("My App")

# #         button = QPushButton("Press Me!")
# #         button.setCheckable(True)
# #         button.clicked.connect(self.the_button_was_clicked)

# #         # Set the central widget of the Window.
# #         self.setCentralWidget(button)

# #     def the_button_was_clicked(self):
# #         print("Clicked!")
# # class MainWindow(QMainWindow):
# #     def __init__(self):
# #         super().__init__()

# #         self.setWindowTitle("My App")

# #         button = QPushButton("Press Me!")
# #         button.setCheckable(True)
# #         button.clicked.connect(self.the_button_was_clicked)
# #         button.clicked.connect(self.the_button_was_toggled)

# #         self.setCentralWidget(button)

# #     def the_button_was_clicked(self):
# #         print("Clicked!")

# #     def the_button_was_toggled(self, checked):
# #         print("Checked?", checked)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("My App")

#         self.button = QPushButton("Press Me!")
#         self.button.clicked.connect(self.the_button_was_clicked)

#         self.setCentralWidget(self.button)

#     def the_button_was_clicked(self):
#         self.button.setText("You already clicked me.")
#         self.button.setEnabled(False)

#         # Also change the window title.
#         self.setWindowTitle("My Oneshot App")
# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

# import sys
# from random import choice

# window_titles = [
#     'My App',
#     'My App',
#     'Still My App',
#     'Still My App',
#     'What on earth',
#     'What on earth',
#     'This is surprising',
#     'This is surprising',
#     'Something went wrong'
# ]


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.n_times_clicked = 0

#         self.setWindowTitle("My App")

#         self.button = QPushButton("Press Me!")
#         self.button.clicked.connect(self.the_button_was_clicked)

#         self.windowTitleChanged.connect(self.the_window_title_changed)

#         # Set the central widget of the Window.
#         self.setCentralWidget(self.button)

#     def the_button_was_clicked(self):
#         print("Clicked.")
#         new_window_title = choice(window_titles)
#         print("Setting title:  %s" % new_window_title)
#         self.setWindowTitle(new_window_title)

#     def the_window_title_changed(self, window_title):
#         print("Window title changed: %s" % window_title)

#         if window_title == 'Something went wrong':
#             self.button.setDisabled(True)


# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()
# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget

# import sys


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("My App")

#         self.label = QLabel()

#         self.input = QLineEdit()
#         self.input.textChanged.connect(self.label.setText)

#         layout = QVBoxLayout()
#         layout.addWidget(self.input)
#         layout.addWidget(self.label)

#         container = QWidget()
#         container.setLayout(layout)

#         # Set the central widget of the Window.
#         self.setCentralWidget(container)


# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()
# import sys

# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.label = QLabel("Click in this window")
#         self.setCentralWidget(self.label)

#     def mouseMoveEvent(self, e):
#         self.label.setText("mouseMoveEvent")

#     def mousePressEvent(self, e):
#         self.label.setText("mousePressEvent")

#     def mouseReleaseEvent(self, e):
#         self.label.setText("mouseReleaseEvent")

#     def mouseDoubleClickEvent(self, e):
#         self.label.setText("mouseDoubleClickEvent")


# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()

# import sys 
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QAction
# from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
    
#     def contextMenuEvent(self, e):
#         context = QMenu(self)
#         context.addAction(QAction("test 1", self))
#         context.addAction(QAction("test 2", self))
#         context.addAction(QAction("test 3", self))
#         context.addAction(QAction("test 4", self))
#         context.exec(e.globalPos())

# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# app.exec()

# import sys

# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import (
#     QApplication,
#     QCheckBox,
#     QComboBox,
#     QDateEdit,
#     QDateTimeEdit,
#     QDial,
#     QDoubleSpinBox,
#     QFontComboBox,
#     QLabel,
#     QLCDNumber,
#     QLineEdit,
#     QMainWindow,
#     QProgressBar,
#     QPushButton,
#     QRadioButton,
#     QSlider,
#     QSpinBox,
#     QTimeEdit,
#     QVBoxLayout,
#     QWidget,
# )


# # Subclass QMainWindow to customize your application's main window
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Widgets App")

#         layout = QVBoxLayout()
#         widgets = [
#             QCheckBox,
#             QComboBox,
#             QDateEdit,
#             QDateTimeEdit,
#             QDial,
#             QDoubleSpinBox,
#             QFontComboBox,
#             QLCDNumber,
#             QLabel,
#             QLineEdit,
#             QProgressBar,
#             QPushButton,
#             QRadioButton,
#             QSlider,
#             QSpinBox,
#             QTimeEdit,
#         ]

#         for w in widgets:
#             layout.addWidget(w())

#         widget = QWidget()
#         widget.setLayout(layout)

#         # Set the central widget of the Window. Widget will expand
#         # to take up all the space in the window by default.
#         self.setCentralWidget(widget)


# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()

# app.exec()