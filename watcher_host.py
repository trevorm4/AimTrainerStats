from utils import *
from watchdog.observers import Observer
from watcher_worker import StatFileHandler

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
    def stop(self):
        self.observer.stop()
        self.observer.join()
    def schedule(self):
        self.observer.schedule(self.handler, self.dir,recursive=True)



