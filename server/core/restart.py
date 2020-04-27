from subprocess import Popen

import psutil

for process in psutil.process_iter():
    if process.cmdline() == ['python', 'checkonlinebooking.py']:
        print('Process found. Terminating it.')
        process.terminate()
        break

git_pull_process = Popen(["git", "pull"])
git_pull_process.wait()

print('Process not found or stopped: starting it.')
Popen(['nohup', 'python3.7', 'checkonlinebooking.py', '&'])
