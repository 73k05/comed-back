import psutil
from subprocess import Popen
import subprocess

for process in psutil.process_iter():
    if process.cmdline() == ['python', 'checkonlinebooking.py']:
        print('Process found. Terminating it.')
        process.terminate()
        break

subprocess.call(["git", "pull"])

print('Process not found or stopped: starting it.')
Popen(['python', 'checkonlinebooking.py'])