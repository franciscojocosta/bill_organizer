import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
class MonitorFolder(FileSystemEventHandler):
    f = ""
    def on_modified(self, event):
        filename = os.path.basename(event.src_path)
        print (filename)
        '''if filename.startswith("985.AR.DP."):
            print("filename")'''

        
    
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