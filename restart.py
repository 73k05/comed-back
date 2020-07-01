from subprocess import Popen

import psutil
import shutil
import datetime

for process in psutil.process_iter():
    try:
        if process.cmdline() == ['python3.7', 'simple_server.py', '&']:
            print('Process found kill simple_server.py Terminating it. -Sarah Conor-')
            process.terminate()
    except ProcessLookupError as err:
        print(f'Error while terminating{err}')
    except FileNotFoundError as err:
        print(f'Error while terminating{err}')

git_pull_process = Popen(["git", "pull"])
git_pull_process.wait()

now = datetime.datetime.now()
shutil.move("output.log", "output" + now.strftime("%d-%m-%y_%H:%M") + ".log")

print('Starting servers...')
Popen(['nohup', 'python3.7', 'simple_server.py', '&'])