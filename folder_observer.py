from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import time

class TextFileEventHandler(PatternMatchingEventHandler):
    def __init__(self, callback, patterns=['*.png'], ignore_patterns=None,
                 ignore_directories=True, case_sensitive=False):
        super().__init__(patterns=patterns, ignore_patterns=ignore_patterns, 
                         ignore_directories=ignore_directories, case_sensitive=case_sensitive)
        self.callback = callback
    
    def on_any_event(self, event):
        print(f"File created: {event.src_path}")
        self.callback()

def start_directory_watch(callback):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fishs")
    event_handler = TextFileEventHandler(callback=callback)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()