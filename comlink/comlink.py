from io import TextIOWrapper
from sys import argv, stdin, stdout, stderr, exit
import sqlite3, time
from os import path, environ


class comlink:
    project_dir:str
    project_name:str
    comlink_file:str
    project_comlink_dir:str
    project_loaded:bool = False
    logfile:TextIOWrapper
    current_id:int = 0
    empty_ids:list[str]
    database:sqlite3.Connection
    char_set:list[str] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    base:int = len(char_set)

    
    def __init__(_):
        _.open_logfile()

        _.project_dir = argv[1]

        if _.project_dir[-1] == '\\':
            _.project_name:str = path.basename(path.normpath(_.project_dir))
        else:
            _.project_name:str = path.basename(_.project_dir)
        _.log(f'project name: {_.project_name}')

        _.current_id = 0
        _.load_project_comlink()
        _.commands = {
            'init': _.load_project_comlink
        }

        _.mainloop()


    def open_logfile(_) -> None: _.logfile = open("comlink-log.txt", 'w+')
    def close_logfile(_) -> None: _.logfile.close()


    def log(_, msg):
        if not hasattr(_, 'logfile'): return
        _.logfile.write(f'[LOG] {msg}\n')
        _.logfile.flush()
        print(msg, file=stderr, flush=True)


    def encode_id(_, id: int) -> str:
        if id == 0: return _.char_set[0]
        chars = ''
        while id > 0:
            id, index = divmod(id, _.base)
            chars += _.char_set[index]
        return chars[::-1]


    def decode_id(_, encoded_id: str) -> int:
        n = 0
        for char in encoded_id:
            n = n * _.base + _.char_set.index(char)
        return n


    def connect_db(_):
        _.database = sqlite3.connect(path.join(_.project_comlink_dir,
                                               f'{_.project_name}.db'))
        _.log("Database connected")
        cursor = _.database.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS"+
                       f"{_.project_name}_comments(id PRIMARY KEY, comment TEXT)")


    def load_comlink_file(_):
        _.log("Loading comlink file...")
        with open(_.comlink_file, 'r') as comlink_file:
            data = comlink_file.readlines()
            _.current_id = int(data[0].split('=')[1])
            _.log(f"Current current_id Value: {_.current_id}")
            _.empty_ids = [id for id in data[1].split('=')[1].split(',')]
            _.log(f"Current Empty IDs: {_.empty_ids}")


    def save_comlink_file(_):
        with open(_.comlink_file, 'w+') as comlink_file:
            comlink_file.write(f'current_id={_.current_id}\n'+
                               f'empty={",".join(_.empty_ids)}')


    def load_project_comlink(_):
        _.log("Loading project's comlink database...")
        if _.project_loaded: return
        if not _.project_loaded: _.project_loaded = True
        _.log("Loading project related comlink")


        _.comlink_file = path.join(_.project_dir, 'comlink', '.comlink')
        if path.exists(_.comlink_file):\
            _.load_comlink_file()
        else:
            with open(_.comlink_file, 'w+') as comlink_file:
                comlink_file.write('current_id=0'+
                                   'empty=')


        _.project_comlink_dir = path.join(_.project_dir, 'comlink')

        if not path.exists(_.project_comlink_dir):
            _.log(f"comlink directory not found in project directory: {_.project_dir}")
            return
        else:
            _.log(f'project comlink dir path: {_.project_comlink_dir}')
            _.db_path = path.join(_.project_comlink_dir, f'{_.project_dir}.db')
            _.log(f'comlink.db path: {_.project_comlink_dir}')
            _.connect_db()


    def get_comment(_, id:str) -> tuple:
        read_cursor = _.database.cursor()
        read_cursor.execute(f"SELECT comment FROM {_.project_name}_comments WHERE id=?",
                            (id,))
        comment = read_cursor.fetchone()
        return comment


    def create_comment__send_id(_, comment) -> None:
        _.log(f"Creating comment: {comment}")
        potential_comment = _.get_comment(_.current_id)
        if potential_comment is None:
            id_str = _.encode_id(_.current_id)
            stdout.write(f'ID:{id_str}\n')
            stdout.flush()
            write_cursor = _.database.cursor()
            write_cursor.execute(f"INSERT INTO {_.project_name}_comments VALUES (?,?)",
                                 (_.current_id, comment))
            _.database.commit()
            _.current_id += 1
            _.save_comlink_file()
        else:
            _.log("ID already exists in comlink database.")


    def get__send_comment(_, id_string:str):
        id = _.decode_id(id_string)
        comment = _.get_comment(id)
        if comment is None:
            _.log("Could not find comment")
            stdout.write(f'{id} is not a valid id\n')
            stdout.flush()
        else:
            stdout.write(f'{comment[0]}\n')
            stdout.flush()


    def safe_stop(_, error=None):
        if environ.get('stopped'): return
        environ.update({'stopped':"1"})

        _.log('Executing safe stop...')

        _.save_comlink_file()

        try: _.close_logfile()
        except Exception as e:
            stderr.write(f"Error closing logfile: {e}")
            stderr.flush()

        stderr.write("Seemed to safely stop comlink")
        stderr.flush()

        time.sleep(0.1) # lil buffer boy
        
        if error: raise error
        else: exit(0)


    def mainloop(_):
        try:
            while True:
                line = stdin.readline()
                if not line: continue
                line = line.strip()
                if line[0] == '@':    _.get__send_comment(line[1:])
                elif line == '!':     _.safe_stop()
                elif line == '*':     _.load_project_comlink()
                elif line[0] == '~':  _.create_comment__send_id(line[1:])
                elif line[0] == '>':  _.commands[line[1:].strip()]()
        except KeyboardInterrupt as e:
            _.safe_stop(e)
        except Exception as e:
            _.safe_stop(e)