from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import time


DOWNLOADS = Path.home() / "Downloads"

# file path for where all ur courses dir exist
UNIVERSITY = Path.home() / "Documents" / "uwaterloo" 

COURSES = ["CS456", "CS454", "CS348", "CS346"]

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        file = Path(event.src_path)
        name = file.name.lower()

        for course in COURSES:
            if course.lower() in name:
                destination = UNIVERSITY / course
                destination.mkdir(parents=True, exist_ok=True)
                print(f"Moving {file} to {destination}")

                if not file.exists():
                    print("file does not exist")
                    return 
            
                shutil.move(
                    str(file),
                    str(destination / file.name)
                )

                print("file moved!")
                break

   

# runs in background and monitors filesystem
observer = Observer()

# only watch the downloads folder for new false
observer.schedule(
    DownloadHandler(),
    str(DOWNLOADS),
    recursive=False
)


observer.start()
print("watching for downlaods...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()