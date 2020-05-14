from subprocess import Popen

import psutil

for process in psutil.process_iter():
    if process.cmdline() == ['python3.7', 'checkonlinebooking.py', '&']:
        print('Process found kill checkonlinebooking.py Terminating it. -Sarah Conor-')
        process.terminate()
    if process.cmdline() == ['python3.7', 'simple_server.py', '&']:
        print('Process found kill simple_server.py Terminating it. -Sarah Conor-')
        process.terminate()

git_pull_process = Popen(["git", "pull"])
git_pull_process.wait()

print('Starting servers...')
Popen(['nohup', 'python3.7', 'checkonlinebooking.py', '&'])
Popen(['nohup', 'python3.7', 'simple_server.py', '&'])
