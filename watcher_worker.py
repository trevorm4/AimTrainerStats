import os
from watchdog.events import RegexMatchingEventHandler
from utils import *

class StatFileHandler(RegexMatchingEventHandler):
    def __init__(self,df):
        self.regex = [r"^*Challenge.*$"]
        self.df = df
        super().__init__(self.regex)

    def on_created(self,event):
        self.process(event)

    def process(self,event):
        stats = create_dict_from_file(event.src_path)
        add_entry(self.df, stats)
