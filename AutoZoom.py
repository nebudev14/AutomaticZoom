from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QObject, QThread, pyqtSignal

import webbrowser
import schedule
import time
import sys

def open_class(url):
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open(url)


schedule.every().day.at("16:50").do(open_class, 'https://us02web.zoom.us/j/87540413095?pwd=NUg1a3c4MlRHZ1VXREpRcmt2WWZDdz09')

# thread running all pending scheduled classes
class Worker(QObject):
    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'AutoZoom'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.schedule_thread()

    # GUI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        name_label = QLabel("Class Name", self)
        name_label.move(20, 20)
        self.name = QLineEdit(self)
        self.name.move(20, 35)
        self.name.resize(280, 30)

        time_label = QLabel("Class Time", self)
        time_label.move(20, 90)
        self.time = QLineEdit(self)
        self.time.move(20, 105)
        self.time.resize(280, 30)

        link_label = QLabel("Class Link", self)
        link_label.move(20, 160)
        self.link = QLineEdit(self)
        self.link.move(20, 175)
        self.link.resize(280, 30)

        # send button
        button = QPushButton("Schedule", self)
        button.setToolTip("Adds the class to your schedule")
        button.move(20, 220)
        button.clicked.connect(self.on_click)

        self.show()

    # connecting GUI to worker thread
    def schedule_thread(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    # opens class meeting link
    def open_class(url):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
        webbrowser.get('chrome').open(url)

    @pyqtSlot()
    def on_click(self):
        self.name.setText("")
        self.time.setText("")
        self.link.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
