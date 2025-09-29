from sys import stderr, exit
from os import environ

def log(msg): print(f'{msg}\n', file=stderr, flush=True)

def safe_stop(*args):
    if environ.get('stopped'): return
    environ.update({'stopped':"1"})
    if args:
        if args[0] == 'error':
            with open("ErrorLog.txt" , 'w') as test:
                test.write(f"Exception: {args[1]}")
                test.flush()
        else:
            signal_number = args[0]
            frame = args[1]
            with open("CleanupLog.txt" , 'w') as test:
                test.write(f"{signal_number}\n{frame}")
                test.flush()
    exit(0)