from utils import *
from watchdog.observers import Observer
from watcher_worker import StatFileHandler
import time
"""
This facilitates monitoring of directory
"""
class StatHost:
    def __init__(self, directory):
        self.dir = directory
        self.df = init_df()
        self.handler = StatFileHandler(self.df)
        self.observer = Observer()
    def start(self):
        self.schedule()
        self.observer.start()
    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    def stop(self):
        self.observer.stop()
        self.observer.join()
    def schedule(self):
        self.observer.schedule(self.handler, self.dir,recursive=True)



