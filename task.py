import subprocess
import time

if __name__ == '__main__':
    cmd = 'python3 luckyNode.py'
    while True:
        start = time.time()
        while True:
            end = time.time()
            if end-start > 21600:
                subprocess.call(cmd.split())
                break