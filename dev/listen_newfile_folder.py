import os
from pickle import TRUE
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
class MonitorFolder(FileSystemEventHandler):
    filename_aux = ""

    def match_substring():
        lal =1

    def edpmatch(self,filename):

        if len(filename) < 12:
            return False

        for i in range(12):
            if filename[i].isnumeric() == False:
                break
            
            if i == 11 and self.filename_aux != filename:

                if len(filename) < 22 and ".pdf" in filename:
                    self.filename_aux = filename
                    return True
               
    def aguamatch(self,filename):
        if "985.AR.DP." in filename and filename != self.filename_aux:
            self.filename_aux = filename
            return TRUE

    def get_agua(self, filename): 
        print (filename)

    def get_edp(self, filename): 
        print (filename)

    def on_modified(self, event):
        filename = os.path.basename(event.src_path)

        if self.aguamatch(filename): self.get_agua(filename)

        elif self.edpmatch(filename): self.get_edp(filename)

        else: print("nada")
  
if __name__ == "__main__":
    src_path = 'C:\\Users\\franc\\Downloads'
    
    event_handler=MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    print("Monitoring started")
    observer.start()
    try:
        while(True):
           time.sleep(1)
           
    except KeyboardInterrupt:
            observer.stop()
            observer.join()