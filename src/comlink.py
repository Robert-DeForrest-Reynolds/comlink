from sys import argv, stdin, stdout, stderr
import sqlite3, atexit, signal, time
from os import path

from util import *

workspace_path = argv[1]
project_comlink_dir = path.join(workspace_path, 'comlink')

# project name is assumed to be the project directory name
project_name:str
if workspace_path[-1] in ['/', '\\']:
    project_name = path.basename(path.normpath(path))
else:
    project_name = path.basename(workspace_path)


db_path = path.join(project_comlink_dir, f'{workspace_path}.db')
database:sqlite3.Connection = None
if path.exists(project_comlink_dir):
    database = sqlite3.connect(path.join(workspace_path, 'comlink', 'db'))



tracker = 0

test_comments = {
}


def create_comment(comment) -> None:
    log(f"Creating comment: {comment}")
    global tracker
    comment_id = tracker
    stdout.write(f'~{comment_id}\n')
    stdout.flush()
    test_comments.update({str(tracker):comment})
    tracker += 1

def cleanup():
    print("Cleaning up before exit...", file=stderr)
    # Save state, close DB, flush logs, etc.

atexit.register(cleanup)

def signal_handler(signum, frame):
    print(f"Signal {signum} received...", file=stderr)
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    while True:
        line = stdin.readline()
        if line == '':
            time.sleep(0.1)  # EOF idle
            continue
        line = line.strip()
        if not line:
            continue
        # handle comments, etc.
finally:
    with open("test.txt" , 'w') as test:
        test.write("hello there")