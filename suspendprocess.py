import psutil
import time

from PyQt5.QtCore import QThread, pyqtSignal



class GTASuspend(QThread):


    seconds = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def gta_v_psid(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.name() == "GTA5.exe":
                    return proc.pid

            except psutil.AccessDenied:
                continue

    def suspend_gta_v(self, psid):
        if psid:
            gta_process = psutil.Process(psid)

            gta_process.suspend()

            seconds = 10

            while seconds != 0:
                time.sleep(1)
                seconds -= 1
                self.seconds.emit(seconds)


            gta_process.resume()


    def run(self):

        processor_id = self.gta_v_psid()

        self.suspend_gta_v(processor_id)









