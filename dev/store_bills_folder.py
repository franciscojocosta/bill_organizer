import os
from pickle import TRUE
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

agua_path = 'C:\\Users\\franc\\Documents\\0 - Documentos\\0 - Contas\\Agua'
edp_path = 'C:\\Users\\franc\\Documents\\0 - Documentos\\0 - Contas\\EDP'
find_path = 'C:\\Users\\franc\\Downloads'

class MonitorFolder(FileSystemEventHandler):
    filename_aux = ""

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
        filepath = os.path.join(find_path,filename) 
        srcpath =  os.path.join(agua_path,filename)
        

        if os.path.isfile(srcpath):
            print("File Already hear")
        else:
            shutil.move(filepath,agua_path)

    def get_edp(self, filename):
        filepath = os.path.join(find_path,filename)
        srcpath =  os.path.join(edp_path,filename)

        if os.path.isfile(srcpath):
            print("File Already hear") 
        else:  
            shutil.move(filepath,edp_path)
        

    def on_modified(self, event):
        filename = os.path.basename(event.src_path)

        if self.aguamatch(filename): self.get_agua(filename)

        elif self.edpmatch(filename): self.get_edp(filename)

        else: print("nada")
  
if __name__ == "__main__":
    
    
    event_handler=MonitorFolder()
    observer = Observer()
    observer.schedule(event_handler, path=find_path, recursive=True)
    print("Monitoring started")
    observer.start()
    try:
        while(True):
           time.sleep(1)
           
    except KeyboardInterrupt:
            observer.stop()
            observer.join()