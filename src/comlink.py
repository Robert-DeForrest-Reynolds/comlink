from sys import argv, stdin, stdout, stderr
import sqlite3, signal, time
from os import path
from random import randrange
from util import *

signal.signal(signal.SIGTERM, safe_stop)

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


def create_comment(comment) -> None:
    log(f"Creating comment: {comment}")
    global tracker
    comment_id = tracker
    stdout.write(f'ID~{comment_id}\n')
    stdout.flush()
    tracker += 1


def get_comment(id:str) -> str:
    return f'{id} is not a valid id'


try:
    while True: 
        line = stdin.readline()
        line = line.strip()
        if not line: continue
        if line[0] == '~':
            create_comment(line)
            continue
            
except Exception as e: safe_stop('error', e)