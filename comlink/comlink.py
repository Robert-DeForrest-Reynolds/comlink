from io import TextIOWrapper
from sys import argv, stdin, stdout, stderr, exit
import sqlite3, signal, time
from os import path, environ
import atexit


class comlink:
    project_dir:str
    project_name:str
    project_comlink_dir:str
    project_loaded:bool = False
    logfile:TextIOWrapper
    tracker:int = 0
    database:sqlite3.Connection
    def __init__(_):
        _.project_dir = argv[1]

        if _.project_dir[-1] == '\\':
            _.project_name:str = path.basename(path.normpath(_.project_dir))
        else:
            _.project_name:str = path.basename(_.project_dir)
        
        _.open_logfile()

        _.log(f'project name: {_.project_name}')

        _.load_project_comlink()

        _.tracker = 0

        _.mainloop()


    def open_logfile(_) -> None: _.logfile = open("comlink-log.txt", 'w+')
    def close_logfile(_) -> None: _.logfile.close()


    def log(_, msg):
        if not hasattr(_, 'logfile'): return
        _.logfile.write(f'[LOG] {msg}\n')
        _.logfile.flush()
        print(msg, file=stderr, flush=True)


    def load_project_comlink(_):
        if _.project_loaded: return
        if not _.project_loaded: _.project_loaded = True
        _.log("Loading project related comlink")
        _.project_comlink_dir = path.join(_.project_dir, 'comlink')

        if not path.exists(_.project_comlink_dir):
            _.log(f"comlink directory not found in project directory: {_.project_dir}")
            return
        else:
            _.log(f'project comlink dir path: {_.project_comlink_dir}')

            _.db_path = path.join(_.project_comlink_dir, f'{_.project_dir}.db')

            _.log(f'comlink.db path: {_.project_comlink_dir}')
            
            _.connect_db()


    def connect_db(_):
        _.database = sqlite3.connect(path.join(_.project_comlink_dir, f'{_.project_name}.db'))


    def increment_and_send_id(_):
        stdout.write(f'ID~{_.tracker}\n')
        stdout.flush()
        _.tracker += 1


    def create_comment(_, comment) -> None:
        _.log(f"Creating comment: {comment}")
        _.increment_and_send_id()
        write_cursor = _.database.cursor()
        write_cursor.execute("INSERT INTO comments ")


    def get_comment(_, id:str) -> str:
        return f'{id} is not a valid id'
    

    def safe_stop(_):
        if environ.get('stopped'): return
        environ.update({'stopped':"1"})

        _.log('Executing safe stop...')
        stdout.flush()
        stderr.flush()

        try:
            _.close_logfile()
        except Exception as e:
            print(f"Error closing logfile: {e}", file=stderr)

        _.log('Safe stop completed')

        time.sleep(0.1) # lil buffer boy
        
        exit(0)


    def mainloop(_):
        try:
            while True:
                line = stdin.readline()
                if not line: continue
                line = line.strip()
                if line == '~':
                    _.safe_stop()
                if line == '*':
                    _.load_project_comlink()
                elif line.startswith('~'):
                    _.create_comment(line)
        except KeyboardInterrupt:
            _.safe_stop('signal', signal.SIGINT, None)
        except Exception as e:
            _.safe_stop('error', e)