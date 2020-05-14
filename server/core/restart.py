from subprocess import Popen

import psutil

for process in psutil.process_iter():
    if process.cmdline() == ['python3.7', 'checkonlinebooking.py', '&']:
        print('Process found kill checkonlinebooking.py Terminating it. -Sarah Conor-')
        try:
            process.terminate()
        except ProcessLookupError as err:
            print(f'Error while terminating{err}')
    if process.cmdline() == ['python3.7', 'simple_server.py', '&']:
        print('Process found kill simple_server.py Terminating it. -Sarah Conor-')
        try:
            process.terminate()
        except ProcessLookupError as err:
            print(f'Error while terminating{err}')

git_pull_process = Popen(["git", "pull"])
git_pull_process.wait()

print('Starting servers...')
Popen(['nohup', 'python3.7', 'checkonlinebooking.py', '&'])
Popen(['nohup', 'python3.7', 'simple_server.py', '&'])
