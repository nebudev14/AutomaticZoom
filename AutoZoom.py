from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import webbrowser
import schedule
import time
import sys

# thread running all pending scheduled classes
class Worker(QObject):
    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

class boxSelect(QComboBox):
    def __init__(self, parent=None):
        super(boxSelect, self).__init__(parent)

class zoomClass():
    def __init__(self, name, link, time):
        self.name = name
        self.link = link
        self.time = time


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'AutoZoom'
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 500
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
        
       # scheduled classes
        self.scheduled_classes_label = QLabel("", self)
        self.scheduled_classes_label.move(475, 20)

        # schedule button
        button = QPushButton("Schedule", self)
        button.setToolTip("Adds the class to your schedule")
        button.move(20, 220)
        button.clicked.connect(self.on_click)

        self.UIComponents()
        self.show()

    # connecting GUI to worker thread
    def schedule_thread(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
    # adds combo box to GUI
    def UIComponents(self):
        # combo box
        self.combo_box = boxSelect(self)
        self.combo_box.setGeometry(200, 150, 50, 30)
        self.combo_box.move(310, 105)
        time = ["AM", "PM"]
        self.combo_box.addItems(time)

    # opens class meeting link
    def open_class(self, url):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
        webbrowser.get('chrome').open(url)

    @pyqtSlot()
    def on_click(self):
        final_name = self.name.text() # name of class that gets added to schedule
        final_link = self.link.text() # zoom/google meets link of class that gets added to schedule
        class_time = str(self.combo_box.currentText()) # morning or afternoon (AM or PM)
        time_num = "" # time of class that gets added to schedule
        try:
            time_text = self.time.text() # gets raw time 
            if len(self.time.text()) == 4: # adds a 0 at the beginning of the time if it only has 3 digits (1:40 becomes 01:40)
                time_text = "0" + time_text
            first_digits = time_text[0] + time_text[1] # first two digits of time
            last_digits = time_text[-2] + time_text[-1]  # last two digits of time
            if class_time == "PM": # adds 12 hours to selected time if class starts in the afternoon
                if first_digits == "12":
                    time_num = first_digits + ":" + last_digits
                else:
                    new_first_digits = str(int(first_digits) + 12)
                    time_num = new_first_digits + ":" + last_digits
            else:
                # sets 12 AM to 00:00 AM
                if first_digits == "12":
                    first_digits = "00"
                time_num = first_digits + ":" + last_digits
            display_time = self.time.text() + class_time # shows time in normal format
            schedule.every().day.at(time_num).do(self.open_class, final_link) # schedules class
            
            # updates scheduled classes display
            prev_text = str(self.scheduled_classes_label.text())
            self.scheduled_classes_label.setText("")
            new_text = prev_text + final_name + " | " + display_time + "\n"
            self.scheduled_classes_label.setText(new_text)
            self.scheduled_classes_label.adjustSize()
            self.name.setText("")
            self.time.setText("")
            self.link.setText("")
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
