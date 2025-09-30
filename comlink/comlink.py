from io import TextIOWrapper
from sys import argv, stdin, stdout, stderr, exit
import sqlite3, signal, time
from os import path, environ
import util


class comlink:
    project_dir:str
    project_name:str
    project_comlink_dir:str
    project_loaded:bool = False
    logfile:TextIOWrapper
    def __init__(_):
        signal.signal(signal.SIGTERM, util.safe_stop)

        _.project_dir = argv[1]

        if _.project_dir[-1] == '\\':
            _.project_name:str = path.basename(path.normpath(path))
        else:
            path.basename(_.project_dir)

        util.log(f'project name: {_.project_name}')

        _.load_project_comlink()

        _.tracker = 0

        _.mainloop()


    def open_logfile(_) -> None: _.logfile = open("comlink-log.txt")
    def close_logfile(_) -> None: _.logfile.close()


    def load_project_comlink(_):
        if _.project_loaded: return
        if not _.project_loaded: _.project_loaded = True
        util.log("Loading project related comlink")
        _.project_comlink_dir = path.join(_.project_dir, 'comlink')

        if not path.exists(_.project_comlink_dir):
            util.log(f"comlink directory not found in project directory: {_.project_dir}")
            util.log(f"comlink needs to be initialized: {_.project_dir}")
            return
        else:
            util.log(f'project comlink dir path: {_.project_comlink_dir}')

            _.db_path = path.join(_.project_comlink_dir, f'{_.project_dir}.db')

            util.log(f'comlink.db path: {_.project_comlink_dir}')
            
            _.connect_db()


    def connect_db(_):
        _.database:sqlite3.Connection = sqlite3.connect(path.join(_.project_comlink_dir, f'{_.project_name}.db'))


    def increment_and_send_id(_):
        global tracker
        comment_id = tracker
        stdout.write(f'ID~{comment_id}\n')
        stdout.flush()
        tracker += 1


    def create_comment(_, comment) -> None:
        util.log(f"Creating comment: {comment}")
        _.increment_and_send_id()


    def get_comment(id:str) -> str:
        return f'{id} is not a valid id'
    

    def safe_stop(_, *args):
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
        _.close_logfile()
        exit(0)


    def mainloop(_):
        try:
            while True: 
                line = stdin.readline()
                line = line.strip()
                if not line: continue
                if line == '*':
                    _.load_project_comlink()
                if line[0] == '~':
                    _.create_comment(line)
                    continue
        except Exception as e: util.safe_stop('error', e)